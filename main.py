import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QTextEdit, QMessageBox, QLabel
from PyQt5.QtCore import *
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

class FileUploader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.file_p = ""

    def init_ui(self):
        self.setWindowTitle('파일 업로더')
        self.setFixedSize(640, 480)

        self.select_file_button = QPushButton('파일 선택')
        self.select_file_button.clicked.connect(self.select_file)

        self.output_label = QLabel('선택된 파일 경로:')

        self.file_path_text_edit = QTextEdit()
        self.file_path_text_edit.setReadOnly(True)
        self.file_path_text_edit.setFixedSize(600, 200)

        self.upload_button = QPushButton('파일 업로드')
        self.upload_button.clicked.connect(self.upload_file)

        self.copy_button = QPushButton('복사')
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        layout = QVBoxLayout()
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.file_path_text_edit)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.copy_button)
        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, '파일 선택', '', 'All Files (*)')
        self.file_p = file_path

        if file_path:
            self.output_label.setText('선택된 파일 경로: ' + file_path)

    def upload_file(self):
        upload_file(self.file_p)

        if self.file_p:
            self.file_path_text_edit.insertPlainText(f"<center>\n   <img src=https://drive.google.com/uc?id={file_id} /><br>\n</center>")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.file_path_text_edit.toPlainText())
        QMessageBox.information(self, "복사 완료", "파일 경로가 클립보드에 복사되었습니다.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    uploader = FileUploader()
    uploader.show()
    sys.exit(app.exec_())