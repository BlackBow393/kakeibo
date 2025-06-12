from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import base64
import mimetypes

def message_base64_encode(message):
    return base64.urlsafe_b64encode(message.as_bytes()).decode()

def attach_file(message, file_path, file_name):
    
    content_type, encoding = mimetypes.guess_type(file_path)
    main_type, sub_type = content_type.split('/',1)
    with open(file_path,'rb') as f:
        message_file = MIMEBase(main_type,sub_type)
        message_file.set_payload(f.read())
    encoders.encode_base64(message_file)
    message_file.add_header(
        'Content-Disposition', 'attachment', filename=file_name
    )
    message.attach(message_file)
    return message

def main():
    scopes = ['https://mail.google.com/']
    creds = Credentials.from_authorized_user_file('token.json',scopes)
    service = build('gmail','v1',credentials=creds)
    
    # ---以下は添付ファイルなしのコード---
    #message = MIMEText('これはPythonからテスト送信しています。\nデスクトップPCのタクミより！')
    #message['To'] = 'bou3.h070215bike@icloud.com'
    #message['From'] = 'm13157mm@gmail.com'
    #message['Subject'] = '送信テスト'
    #raw = {'raw':message_base64_encode(message)}
    
    #service.users().messages().send(
        #userId='me',
        #body=raw
    #).execute()
    
    # ---以下は添付ファイルありのコード---
    message = MIMEMultipart()
    message['To'] = 'bou3.h070215bike@icloud.com'
    message['From'] = 'm13157mm@gmail.com'
    message['Subject'] = '送信テスト添付ファイル付'
    message.attach(MIMEText('添付ファイルを送信します。','plain'))
    
    message = attach_file(message,'./image_3.jpg','image_3.jpg')
    
    raw = {'raw': message_base64_encode(message)}
    service.users().messages().send(
        userId='me',
        body=raw
    ).execute()

if __name__ == '__main__':
    main()