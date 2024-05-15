from googleapiclient.discovery import build
from google.oauth2 import service_account

scopes = ['https://www.googleapis.com/auth/drive']
service_account_file = "image-upload-423409-6c68e51e6af7.json"
folder_id = "1sIaAiwBVWALcZM4O4hwDDEkHNuxsXJXA"

file_id = ""

def authenticate():
    creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
    return creds

def upload_file(file_path):
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

upload_file("shutterstock_2205178589-1-1.png")

print(f"<center>\n<img src=https://drive.google.com/uc?id={file_id} /><br>\n</center>")