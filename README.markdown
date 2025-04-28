# Resume Analyzer

This repository contains a Flask-based web application designed to analyze resumes for AI school admissions. The application allows users to upload resumes in `.docx` or `.pdf` formats, extracts text from the uploaded files, and evaluates the candidate's suitability based on their academic level (First Year to Fourth Year) using the Mistral AI API.

## Features

- **Resume Upload**: Supports `.docx` and `.pdf` file formats with a maximum file size of 16 MB.
- **Text Extraction**: Extracts text from uploaded resumes using `python-docx` for `.docx` files and `PyPDF2` for `.pdf` files.
- **Candidate Evaluation**: Analyzes resumes based on the student's academic level (First Year to Fourth Year) and provides a score (out of 10) along with reasoning.
- **Dynamic Level Detection**: Determines the student's academic level based on the upload page (pge1 to pge4).
- **Secure File Handling**: Ensures secure file uploads using `werkzeug.utils.secure_filename` and removes uploaded files after processing.

## Project Structure

```
resume-analyzer/
├── app.py                  # Main Flask application
├── resume_analyzer.py      # Resume text extraction and evaluation logic
├── templates/
│   ├── upload.html         # Template for the upload page
│   ├── result.html         # Template for displaying evaluation results
├── uploads/                # Temporary folder for uploaded files
├── .env                    # Environment variables (not included in repo)
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- A Mistral AI API key (set in a `.env` file)
- Required Python packages (listed in `requirements.txt`)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/resume-analyzer.git
   cd resume-analyzer
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - `flask`
   - `python-dotenv`
   - `werkzeug`
   - `python-docx`
   - `PyPDF2`
   - `requests`

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add your Mistral AI API key:
   ```
   MISTRAL_API_KEY=your_mistral_api_key
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will run on `http://127.0.0.1:5000` in debug mode.

## Usage

1. **Access the Application**:
   Open a web browser and navigate to `http://127.0.0.1:5000`.

2. **Upload a Resume**:
   - Select a `.docx` or `.pdf` resume file from one of the upload fields (corresponding to First Year, Second Year, Third Year, or Fourth Year).
   - Submit the form to upload the file.

3. **View Results**:
   - The application extracts the resume text and evaluates it using the Mistral AI API.
   - Results are displayed on the `result.html` page, including the extracted text, candidate score, and reasoning.

## Evaluation Criteria

The evaluation is tailored to the student's academic level:
- **First Year (pge1)**: Focuses on foundational skills, coding basics, math fundamentals, and AI/ML interest.
- **Second Year (pge2)**: Expects intermediate skills and growing AI/ML knowledge.
- **Third Year (pge3)**: Looks for advanced coursework and project experience.
- **Fourth Year (pge4)**: Emphasizes advanced ML techniques, research projects, and internships.

The Mistral AI API returns a JSON response with:
- Full name
- Email address
- Current academic level
- Score (out of 10)
- Reasoning for the score

## Security Considerations

- **File Uploads**: Only `.docx` and `.pdf` files are allowed, and filenames are sanitized using `secure_filename`.
- **File Management**: Uploaded files are stored temporarily in the `uploads/` folder and deleted after processing.
- **Size Limits**: Maximum upload size is set to 16 MB to prevent abuse.

## Limitations

- Requires a valid Mistral AI API key for resume evaluation.
- Only supports `.docx` and `.pdf` file formats.
- The application assumes the upload page (pge1 to pge4) corresponds to the student's academic level.
- Error handling for API failures returns a JSON error response.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or issues, please open an issue on GitHub or contact shafiyakausar123@gmail.com.