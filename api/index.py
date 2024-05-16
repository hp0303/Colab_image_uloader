import os
from flask import Flask, render_template, request
from googleapiclient.discovery import build
from google.oauth2 import service_account

scopes = ['https://www.googleapis.com/auth/drive']
service_account_file = "../image-upload-423409-6c68e51e6af7.json"
folder_id = "1sIaAiwBVWALcZM4O4hwDDEkHNuxsXJXA"

file_id = ""

def authenticate():
    creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
    return creds

def upload_file_drive(file_path):
    global file_id
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_path,
        'parents': [folder_id]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()
    file_id = file.get("id")


app = Flask(__name__)

UPLOAD_FOLDER = 'image'  # 이미지를 저장할 폴더명
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # 파일을 업로드하고 저장하는 로직
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

            print(file_path)

            upload_file_drive(str(file_path))
            global file_id

            os.remove(file_path)

            return render_template('index.html', message='File uploaded successfully!', filename=f"<center>\n<img src=https://drive.google.com/uc?id={file_id} /><br>\n</center>")

    return render_template('index.html', message='File uploaded Failed')
