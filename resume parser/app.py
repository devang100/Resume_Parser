from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from pyresparser import ResumeParser
import os

app = Flask(__name__)

# Set the folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Call your resume parser function here
        parsed_data = parse_resume(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('result.html', data=parsed_data)
    return redirect(url_for('index'))

def parse_resume(file_path):
    data = ResumeParser(file_path).get_extracted_data()
    
    # Extracting individual fields
    name = data.get('name', '')
    email = data.get('email', '')
    experience = '\n'.join(data.get('experience', []))
    skills = '\n'.join(data.get('skills', []))
    education = '\n'.join(data.get('education', []))

    return {
        'name': name,
        'email': email,
        'experience': experience,
        'skills': skills,
        'education': education
    }

if __name__ == '__main__':
    app.run(debug=True)
