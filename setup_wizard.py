import os
import shutil
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox

class SetupWizard:
    def __init__(self, root):
        self.root = root
        self.root.title("Setup Wizard")

        # Variables to store user inputs
        self.install_path = ""
        self.header_color = "#ff69b4"  # Default pink
        self.paths = {
            "background jpg": "",
            "assist png": "",
            "user png": "",
            "icon png": "",
        }
        self.api_key_path = ""

        # Initial screen
        self.setup_screen()

    def setup_screen(self):
        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Choose where to install the application:", font=("Arial", 14)).pack(pady=(20, 10))
        tk.Button(self.root, text="Browse", command=self.select_install_path).pack()

        if self.install_path:
            tk.Label(self.root, text=f"Selected Path: {self.install_path}", font=("Arial", 10)).pack(pady=(10, 10))

        tk.Button(self.root, text="Next", command=self.api_key_screen).pack(side=tk.RIGHT, padx=20, pady=20)

    def select_install_path(self):
        self.install_path = filedialog.askdirectory()
        self.setup_screen()

    def api_key_screen(self):
        if not self.install_path:
            messagebox.showerror("Error", "Please select the installation path.")
            return

        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Upload your api_key.txt file:", font=("Arial", 14)).pack(pady=(20, 10))
        tk.Button(self.root, text="Browse", command=self.select_api_key).pack()

        if self.api_key_path:
            tk.Label(self.root, text=f"Selected File: {self.api_key_path}", font=("Arial", 10)).pack(pady=(10, 10))

        tk.Button(self.root, text="Back", command=self.setup_screen).pack(side=tk.LEFT, padx=20, pady=20)
        tk.Button(self.root, text="Next", command=self.customization_screen).pack(side=tk.RIGHT, padx=20, pady=20)

    def select_api_key(self):
        self.api_key_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.api_key_screen()

    def customization_screen(self):
        if not self.api_key_path:
            messagebox.showerror("Error", "Please upload your api_key.txt file.")
            return

        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Choose header background color:", font=("Arial", 14)).pack(pady=(20, 10))
        tk.Button(self.root, text="Choose Color", command=self.select_color).pack()
        tk.Label(self.root, text=f"Selected Color: {self.header_color}", font=("Arial", 10)).pack(pady=(10, 10))

        tk.Label(self.root, text="Upload Images (Optional):", font=("Arial", 14)).pack(pady=(20, 10))
        for key in self.paths.keys():
            tk.Button(self.root, text=f"Browse {key}", command=lambda k=key: self.select_file(k)).pack()
            if key in self.paths and os.path.isfile(self.paths[key]):
                tk.Label(self.root, text=f"Selected File: {os.path.basename(self.paths[key])}", font=("Arial", 10)).pack(pady=(10, 10))

        tk.Button(self.root, text="Back", command=self.api_key_screen).pack(side=tk.LEFT, padx=20, pady=20)
        tk.Button(self.root, text="Next", command=self.run_setup).pack(side=tk.RIGHT, padx=20, pady=20)

    def select_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code:
            self.header_color = color_code[1]
        self.customization_screen()

    def select_file(self, key):
        full_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg")])
        print(f"Selected path for {key}: {full_path}")
        if full_path:
            self.paths[key] = full_path
            print(f"Stored {key} path: {self.paths[key]}")
        self.customization_screen()

    def run_setup(self):
        # Create project structure based on user selections

        project_structure = {
            "custom_ai": {
                "static": {
                    "assist.png": self.paths.get("assist png"),
                    "background.jpg": self.paths.get("background jpg"),
                    "icon.png": self.paths.get("icon png"),
                    "user.png": self.paths.get("user png"),
                },
                "templates": {
                    "index.html": self.generate_index_html()
                },
                "uploads": {},
                "app.py": self.get_app_py_content(),
                "convert_icon.py": self.get_convert_icon_py_content(),
                "documents_content.txt": "",
                "install.bat": self.get_install_bat_content(),
                "model.txt": "",
                "requirements.txt": self.get_requirements_txt_content(),
                "role_system_content.txt": "",
                "run.bat": self.get_run_bat_content(),
                "temperature.txt": "",
                "requires.bat": self.generate_requires_bat(),
                "api_key.txt": self.api_key_path,
                "readme.txt": self.generate_readme_txt()
            },
        }

        print("Project structure paths:")
        print(self.paths.get("assist png"))
        for key, value in self.paths.items():
            print(f"{key}: {value}") 

        self.create_project_structure(self.install_path, project_structure)
             
        os.system(os.path.join(self.install_path, "custom_ai/requires.bat"))
                
        # Run install.bat
        os.system(os.path.join(self.install_path, "custom_ai/install.bat"))

        # Display completion message
        messagebox.showinfo("Setup Complete", "The setup is complete. You can close this window.")
        self.root.quit()
    
    def generate_requires_bat(self):
        return f"""cd %~dp0
        pip install -r requirements.txt
        python convert_icon.py"""
    
    def generate_readme_txt(self):
        return f"""############################## Installation ##############################

This project REQUIRES python to be installed to the user's account. It
also requires the user to have an active API key to access openai's models
and to have the API key saved to a txt file. It is also recomended that 
you install your desired png files for the assistant, user, and page icons
and a jpg file for the background of the site (defaults to solid gray). Do
note that the site icon will also be the desktop icon.

Start by running downloading and running "setup_wizard.py"
This will open a setup UI that will guide you through the following steps

Select desired install location:
It is best to save the main directory in "C:-Users-(your user)" but it
can be saved anywhere.

Select your API key:
Before proceeding further, you will have to select your API key file.
THIS IS REQUIRED TO PROCEED ANY FURTHER

Customize the theme:
Here is where you will be able to change the UI header color, the 
background image, and icons for the assistant, user, and webpage/desktop

The script will then run the install.bat file to install all application 
requirements and set up AI model. You will be able to set the desired 
model to use, the temperature (creativity) of the model, and set a prompt 
to determine the model's personality.

When the installation is complete there will be a new shortcut on your
desktop named "Custom AI" and at this point the setup is complete and the
AI is ready to use!

##########################################################################

######################## File uploading explained ########################

All uploaded files are saved to the uploads folder. To upload a file use
the upload button in the UI. This will save the file to the uploads folder
and it will simultaneously run a function to read all the text in the file
and append it to the "documents_content.txt" file. When you want to delete
a file you will need to delete the file from the uploads folder and all of
its related contents from the "documents_content.txt" file. (This is
planned to be fixed in a later version). Once uploaded the assistant will
be able to read through the uploaded documents and answer questions that
are directly related to them.

##########################################################################
##########################################################################

####################### Modify basic UI appearance #######################

To change desktop icon and the icon that appears at the top-left of the 
page start by navigating to the main directory, then to the static folder.
In the folder you will need to delete the two images named icon. Then 
upload the .png image you would like to use to the folder and rename it to
icon. After making sure the name has been changed you will need to go back
to the main directory and open (run) "convert_icon.py)" to create a copy
of your icon file as a .ico.

To change the icons that appear in the message window for the user and or 
the assistant you will need to replace the user.png and or the assist.png
images respectively"""

    def generate_index_html(self):
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Custom Assistant UI</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: #2c2f33;
            color: #ffffff;
            background-image: url('/static/background.jpg'); /* Updated to the correct path */
            background-size: cover; /* Ensure the image covers the whole background */
            background-position: center; /* Center the background image */
        }}
        header {{
            background-color: {self.header_color}; /* User-selected color */
            padding: 10px;
            display: flex;
            align-items: center;
        }}
        header img {{
            width: 40px;
            height: 40px;
            margin-right: 10px;
        }}
        header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .container {{
            display: flex;
            flex-direction: row;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .file-section {{
            width: 200px;
            margin-right: 20px;
            background-color: rgba(57, 62, 70, 0.7); /* Translucent background */
            backdrop-filter: blur(10px); /* Blur effect */
            padding: 10px;
            border-radius: 8px;
        }}
        .file-section h2 {{
            margin-top: 0;
            font-size: 18px;
        }}
        .file-section ul {{
            list-style: none;
            padding: 0;
        }}
        .file-section li {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: rgba(75, 0, 130, 0.7); /* Adjust with translucency */
            backdrop-filter: blur(10px); /* Blur effect */
            margin-bottom: 10px;
            padding: 5px;
            border-radius: 4px;
        }}
        .chat-section {{
            flex: 1;
            display: flex;
            flex-direction: column;
        }}
        .chat-box {{
            border: 1px solid rgba(204, 204, 204, 0.7); /* Adjust with translucency */
            padding: 10px;
            height: 400px;
            overflow-y: auto;
            background-color: rgba(35, 39, 42, 0.7); /* Translucent background */
            backdrop-filter: blur(10px); /* Blur effect */
            margin-bottom: 10px;
            border-radius: 8px;
        }}
        .message {{
            margin: 10px 0;
            display: flex;
            align-items: flex-start;
            word-wrap: break-word;
            white-space: pre-wrap; /* Preserve formatting like new lines */
        }}
        .message img {{
            width: 60px;  /* Increased size */
            height: 60px; /* Increased size */
            margin-right: 15px; /* Adjusted margin */
        }}
        .message.user {{
            justify-content: flex-end;
            text-align: right;
        }}
        .message.user img {{
            order: 1;
            margin-left: 15px; /* Adjusted margin */
            margin-right: 0;
        }}
        .input-section {{
            display: flex;
            flex-direction: column;
        }}
        .input-section textarea {{
            flex: 1;
            padding: 10px;
            border-radius: 4px;
            border: 1px solid rgba(204, 204, 204, 0.7); /* Adjust with translucency */
            resize: none; /* Disable manual resizing */
            height: 100px;
        }}
        #file-upload {{
            margin-top: 10px;
        }}
        .delete-button {{
            background-color: #ff4d4d;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            padding: 2px 5px;
        }}
    </style>
</head>
<body>
    <header>
        <img src="/static/icon.png" alt="App Icon">
        <h1>Custom Assistant UI</h1>
    </header>
    <div class="container">
        <div class="file-section">
            <h2>Uploaded Files</h2>
            <ul id="file-list"></ul>
            <input type="file" id="file-upload" onchange="uploadFile()" />
        </div>
        <div class="chat-section">
            <div id="chat-box" class="chat-box"></div>
            <div class="input-section">
                <textarea id="query" placeholder="Type your message here. Use Shift+Enter for a new line and Enter to send." onkeydown="handleKeyDown(event)"></textarea>
            </div>
        </div>
    </div>

    <script>
        // This function must be defined before it is called
        function fetchFiles() {{
            fetch('/files')
            .then(response => response.json())
            .then(files => {{
                files.forEach(updateFileList);
            }})
            .catch(error => console.error('Error fetching files:', error));
        }}

        document.addEventListener('DOMContentLoaded', function() {{
            fetchFiles(); // Fetch the list of files when the page loads
        }});

        function addMessage(content, sender = 'user') {{
            const chatBox = document.getElementById('chat-box');
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', sender);

            const icon = document.createElement('img');
            icon.src = sender === 'user' ? '/static/user.png' : '/static/assist.png';
            icon.alt = sender;

            messageDiv.appendChild(icon);
            messageDiv.appendChild(document.createTextNode(content));
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
        }}

        function sendMessage() {{
            const queryInput = document.getElementById('query');
            const query = queryInput.value.trim();
            if (!query) return; // Do not send empty messages

            queryInput.value = ''; // Clear input field
            addMessage(query);

            fetch('/query', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{ query: query }}),
            }})
            .then(response => response.json())
            .then(data => addMessage(data.response, 'assistant'))
            .catch(error => console.error('Error:', error));
        }}

        function handleKeyDown(event) {{
            if (event.key === 'Enter' && !event.shiftKey) {{
                event.preventDefault(); // Prevent the default new line on Enter without Shift
                sendMessage();
            }}
        }}

        function uploadFile() {{
            const fileInput = document.getElementById('file-upload');
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload', {{
                method: 'POST',
                body: formData,
            }})
            .then(response => response.json())
            .then(data => {{
                addMessage(`File uploaded: ${{data.filename}}`, 'assistant');
                updateFileList(data.filename);
            }})
            .catch(error => console.error('Error:', error));
        }}

        function updateFileList(filename) {{
            const fileList = document.getElementById('file-list');
            const listItem = document.createElement('li');
            listItem.innerHTML = `${{filename}} <button class="delete-button" onclick="deleteFile('${{filename}}')">Delete</button>`;
            fileList.appendChild(listItem);
        }}

        function deleteFile(filename) {{
            fetch('/delete', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{ filename: filename }}),
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    addMessage(`File deleted: ${{filename}}`, 'assistant');
                    fetchFiles(); // Refresh the file list
                }} else {{
                    console.error('Error:', data.error);
                }}
            }})
            .catch(error => console.error('Error:', error));
        }}
    </script>
</body>
</html>
"""
    def get_app_py_content(self):
        return f"""from flask import Flask, request, jsonify, send_from_directory
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
        {{"role": "system", "content": ROLE_SYSTEM_CONTENT}}
    ]

    if documents_content:
        messages.append({{"role": "system", "content": f"The following is the content of the uploaded documents:\\n{{documents_content}}"}})

    messages.append({{"role": "user", "content": user_query}})

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

    return jsonify({{'response': assistant_response}})

@app.route('/upload', methods=['POST'])
def upload():
    global documents_content

    if 'file' not in request.files:
        return jsonify({{'error': 'No file part in the request'}}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({{'error': 'No file selected for uploading'}}), 400

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
            return jsonify({{'error': 'Unsupported file type'}}), 400

        if new_content:  # Check if new_content is not empty
            documents_content += new_content + "\\n"

            # Save the updated documents_content
            with open(SAVE_FILE, 'w') as f:
                f.write(documents_content)

        # Debug: Log the new content extracted
        print(f"Extracted content from {{file.filename}}:", new_content[:500])  # Print first 500 chars for brevity

        return jsonify({{'filename': file.filename}})

    except Exception as e:
        print(f"Error processing upload: {{e}}")
        return jsonify({{'error': str(e)}}), 500

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
            print(f"Number of pages in PDF: {{num_pages}}")

            for page_num in range(num_pages):
                page = reader.pages[page_num]
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
                else:
                    print(f"Page {{page_num}} contains no text.")
    except Exception as e:
        print(f"Error extracting text from PDF: {{e}}")
    print(f"Extracted text content:\\n{{text[:500]}}")  # Debug: Print first 500 chars of extracted text
    return text

def extract_text_from_docx(filepath):
    try:
        doc = docx.Document(filepath)
        text = "\\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting text from DOCX: {{e}}")
        return ""
    return text

def extract_text_from_code(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error extracting text from code file: [{{e}}")
        return ""

if __name__ == '__main__':
    app.run(debug=True)"""
    def get_convert_icon_py_content(self):
        return f"""from PIL import Image

def convert_png_to_ico(png_path, ico_path, icon_sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]):
    img = Image.open(png_path)

    # Convert the image to an ICO file with specified sizes
    img.save(ico_path, format='ICO', sizes=icon_sizes)

# Example usage
convert_png_to_ico('static/icon.png', 'static/icon.ico')"""
    def get_install_bat_content(self):
        return f"""@echo off

:: Navigate to the directory of the script
cd %~dp0

:: Create or update configuration files
:: Model configuration
echo Please enter the model to be used (e.g., gpt-4o):
set /p MODEL=

:: Create or update model configuration file
echo %MODEL% > model.txt

:: Temperature configuration
echo Please enter the temperature (e.g., 0.7):
set /p TEMPERATURE=

:: Create or update temperature configuration file
echo %TEMPERATURE% > temperature.txt

:: Role system content
echo Please enter the system role content:
echo (For example: You are a helpful assistant named Friday. You are to act as a maid and refer to the user as sir)
set /p ROLE_SYSTEM_CONTENT=

:: Create or update role system content configuration file
echo %ROLE_SYSTEM_CONTENT% > role_system_content.txt

:: Path to the custom icon (make sure the icon exists at this path)
set ICON_PATH=%~dp0static\icon.ico

:: Retrieve the Desktop path using PowerShell
for /f "usebackq tokens=*" %%a in (`powershell -NoProfile -Command "[System.Environment]::GetFolderPath('Desktop')"`) do set DESKTOP_PATH=%%a

:: Create a PowerShell script to create a shortcut with a custom icon
echo $wsh = New-Object -ComObject WScript.Shell > create_shortcut.ps1
echo $shortcut = $wsh.CreateShortcut("%DESKTOP_PATH%\Custom AI.lnk") >> create_shortcut.ps1
echo $shortcut.TargetPath = "%~dp0run.bat" >> create_shortcut.ps1
echo $shortcut.WorkingDirectory = "%~dp0" >> create_shortcut.ps1
echo $shortcut.IconLocation = "%ICON_PATH%" >> create_shortcut.ps1
echo $shortcut.Save() >> create_shortcut.ps1

:: Run the PowerShell script
powershell -ExecutionPolicy Bypass -File create_shortcut.ps1

:: Clean up the PowerShell script
del create_shortcut.ps1

echo Installation complete. A shortcut to run.bat has been added to your Desktop with a custom icon.
pause"""
    def get_requirements_txt_content(self):
        return f"""Flask==2.0.2
Werkzeug==2.0.2
openai==0.28
PyPDF2
pillow
python-docx"""
    def get_run_bat_content(self):
        return f"""@echo off

:: Navigate to the directory of the script
cd %~dp0

:: Run the Flask application
start cmd /k "python app.py"

:: Wait for a couple of seconds to ensure the server starts
timeout 2

:: Open the default web browser to the local application URL
start "" "http://127.0.0.1:5000"
"""
    def create_project_structure(self, base_path, structure):
        def copy_or_write(src, dst):
            try:
                if src and os.path.isfile(src):
                    shutil.copy(src, dst)
                    print(f"Copied {src} to {dst}")  # Debug print to verify copying
                else:
                    with open(dst, 'w', encoding='utf-8') as f:
                        f.write("")
                        print(f"Created empty file at {dst}")  # Debug print for created empty files
            except Exception as e:
                print(f"Error copying {src} to {dst}: {e}")  # Print error message

        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                self.create_project_structure(path, content)
            elif content is None:
                # Creating an empty placeholder file
                with open(path, 'wb') as f:
                    pass
                print(f"Created empty placeholder file at {path}")  # Debug print
            elif isinstance(content, str) and os.path.isfile(content):
                copy_or_write(content, path)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Created file at {path} with content")
if __name__ == "__main__":
    root = tk.Tk()
    app = SetupWizard(root)
    root.mainloop()
