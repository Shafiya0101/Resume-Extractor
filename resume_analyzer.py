import os
import json
import requests
import docx
import PyPDF2

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return "\n".join(text)

def extract_text(file):
    filename = file.filename.lower()
    if filename.endswith('.docx'):
        return extract_text_from_docx(file)
    elif filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    else:
        raise ValueError("Unsupported file type. Please upload a .docx or .pdf file.")

def classify_candidate(resume_text, page_name):
    """
    Analyze resume for AI school admission based on student level.
    
    Args:
        resume_text (str): Text content of the resume
        page_name (str): Page/level identifier (pge1, pge2, pge3, pge4)
    
    Returns:
        dict: Resume evaluation with score and reasoning
    """
    BASE_URL = "https://api.mistral.ai/v1"
    API_KEY = os.getenv('MISTRAL_API_KEY')
    
    # Determine student level based on page name
    level_mapping = {
        'pge1': 'First Year',
        'pge2': 'Second Year',
        'pge3': 'Third Year',
        'pge4': 'Fourth Year'
    }
    current_level = level_mapping.get(page_name.lower(), 'Unknown')
    
    instruction = f'''
    You are an AI bot grading resumes for an AI school admission. 
    The student is at the {current_level} level.
    
    Grading Criteria:
    - Adjust skill weights based on the student's current level
    - First Year: Programming Proficiency (40%), Mathematical Foundations (30%), Exploration and Curiosity (20%), Participation and Collaboration (10%)
    - Second Year: Data Visualization Skills (25%), ML Basics and Implementation (30%), Computer Science Fundamentals (25%), Project Quality and Innovation (15%), Communication Skills (5%)
    - Third Year: Deep Learning Mastery (30%), Business Management and Strategy (25%), Intermediate ML Implementation (20%),Team Projects and Leadership (15%), Ethical AI Practices (10%)
    - Fourth Year: Expect advanced AI skills, research, practical experience
    
    Return a JSON with:
    - Full name as full_name
    - Email address as email
    - Current level as current_level
    - Score (out of 10) as score
    - Reasoning behind the score as reasoning
    
    Key Considerations:
    - First Year: Coding basics, math fundamentals, AI/ML interest
    - Second Year: Data visualization, ML, Computer science
    - Third Year: Deep Learning, ML, Business Management
    - Fourth Year: Advanced ML techniques, research projects, internships
    
    Do not generate any text other than the JSON response.
    '''
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    payload = {
        'model': 'mistral-medium',
        'messages': [
            {'role': 'system', 'content': instruction},
            {'role': 'user', 'content': resume_text}
        ],
        'max_tokens': 2000,
        'temperature': 0.7
    }
    
    try:
        response = requests.post(f'{BASE_URL}/chat/completions', 
                                 json=payload, 
                                 headers=headers)
        
        response.raise_for_status()
        
        result = response.json()['choices'][0]['message']['content']
        return json.loads(result)
    
    except requests.RequestException as e:
        print(f"Error generating text: {e}")
        return {
            "error": "Could not process resume evaluation",
            "details": str(e)
        }