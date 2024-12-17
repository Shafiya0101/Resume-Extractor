import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

from resume_analyzer import extract_text, classify_candidate

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'docx', 'pdf'}

def allowed_file(filename):
    """Return True if the given filename is an allowed type, False otherwise.

    Checks if the given filename has a file extension, and if that
    extension is in the set of ALLOWED_EXTENSIONS.
    """
    return '.' in filename and \
           filename.lower().split('.')[-1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    """Handles upload of resume for analysis.
    
    When a POST request is received, this function determines which file was
    uploaded, checks if it is an allowed type, extracts the text from the
    uploaded file, analyzes the resume using the ``classify_candidate``
    function, and renders a template with the evaluation results.
    
    If any errors occur during this process, the function returns an error
    message as a JSON response with a 400 or 500 status code.
    
    When a GET request is received, this function simply renders the
    'upload.html' template.
    """
    
    if request.method == 'POST':
        # Set default page_level and file
        page_level = 'pge1'  # Default
        file = None

        # Check each file input
        if 'resume' in request.files and request.files['resume'].filename:
            file = request.files['resume']
            page_level = 'pge1'
        elif 'resume2' in request.files and request.files['resume2'].filename:
            file = request.files['resume2']
            page_level = 'pge2'
        elif 'resume3' in request.files and request.files['resume3'].filename:
            file = request.files['resume3']
            page_level = 'pge3'
        elif 'resume4' in request.files and request.files['resume4'].filename:
            file = request.files['resume4']
            page_level = 'pge4'
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Extract text from uploaded resume
                resume_text = extract_text(file)
                
                # Analyze resume with dynamically detected level
                evaluation = classify_candidate(resume_text, page_level)
                
                # Remove uploaded file after processing
                os.remove(filepath)
                
                return render_template('result.html', 
                                       resume_text=resume_text, 
                                       evaluation=evaluation)
            
            except Exception as e:
                # Remove file in case of error
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({"error": str(e)}), 500
        
        return jsonify({"error": "Invalid file type. Please upload a .docx or .pdf file"}), 400
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)