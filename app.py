from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from PyPDF2 import PdfReader  # Updated import for PdfReader
import docx

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SAVE_FILE = 'documents_content.txt'

# Function to read configuration
def read_config(file_path, default_value):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read().strip()
    return default_value

# Reading configuration from files
API_KEY = read_config('api_key.txt', '0')
MODEL = read_config('model.txt', 'gpt-4o')  # Default model is 'gpt-4o'
TEMPERATURE = float(read_config('temperature.txt', '1.0'))  # Default temperature is 1.0
ROLE_SYSTEM_CONTENT = read_config('role_system_content.txt', 'You are a helpful assistant named Friday. You are to act as a maid and refer to the user as sir')  # Default system role content

# Set your OpenAI API key here
openai.api_key = API_KEY

# Initialize documents_content with the content of the save file if it exists
documents_content = ""
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, 'r') as f:
        documents_content = f.read()

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/query', methods=['POST'])
def query():
    global documents_content

    data = request.get_json()
    user_query = data.get('query')

    # Debug: Log the incoming query and current document content
    print("Received query:", user_query)
    print("Current document content:", documents_content[:500])  # Print first 500 chars for brevity

    # Prepare the messages with document content included
    messages = [
        {"role": "system", "content": ROLE_SYSTEM_CONTENT}
    ]

    if documents_content:
        messages.append({"role": "system", "content": f"The following is the content of the uploaded documents:\n{documents_content}"})

    messages.append({"role": "user", "content": user_query})

    # Call to OpenAI API with the user query and documents content as context
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=4000
    )

    assistant_response = response["choices"][0]["message"]["content"].strip()

    # Debug: Log the assistant's response
    print("Assistant response:", assistant_response)

    return jsonify({'response': assistant_response})

@app.route('/upload', methods=['POST'])
def upload():
    global documents_content

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Extract content from the uploaded file based on its type
        new_content = ""
        if file.filename.endswith('.pdf'):
            new_content = extract_text_from_pdf(filepath)
        elif file.filename.endswith('.docx'):
            new_content = extract_text_from_docx(filepath)
        elif file.filename.endswith(('.py', '.js', '.java', '.txt', '.c', '.cpp', '.rb', '.html', '.css')):
            new_content = extract_text_from_code(filepath)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        if new_content:  # Check if new_content is not empty
            documents_content += new_content + "\n"

            # Save the updated documents_content
            with open(SAVE_FILE, 'w') as f:
                f.write(documents_content)

        # Debug: Log the new content extracted
        print(f"Extracted content from {file.filename}:", new_content[:500])  # Print first 500 chars for brevity

        return jsonify({'filename': file.filename})

    except Exception as e:
        print(f"Error processing upload: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

def extract_text_from_pdf(filepath):
    text = ""
    try:
        with open(filepath, 'rb') as f:
            reader = PdfReader(f)
            num_pages = len(reader.pages)
            
            # Debug: Log the number of pages
            print(f"Number of pages in PDF: {num_pages}")

            for page_num in range(num_pages):
                page = reader.pages[page_num]
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
                else:
                    print(f"Page {page_num} contains no text.")
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    print(f"Extracted text content:\n{text[:500]}")  # Debug: Print first 500 chars of extracted text
    return text

def extract_text_from_docx(filepath):
    try:
        doc = docx.Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""
    return text

def extract_text_from_code(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error extracting text from code file: {e}")
        return ""

if __name__ == '__main__':
    app.run(debug=True)