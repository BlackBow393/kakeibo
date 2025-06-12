from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import os

def base64_decode_file(data):
    return base64.urlsafe_b64decode(data.encode('UTF-8'))

def save_attachments_from_email(settings):
    creds = Credentials.from_authorized_user_file('token.json', ['https://mail.google.com/'])
    service = build('gmail', 'v1', credentials=creds)

    # 受信メールを検索（全件、または件名に基づいて絞り込み）
    for subject, save_folder in settings:
        query = f"subject:{subject}"
        messages_response = service.users().messages().list(userId='me', q=query).execute()
        messages = messages_response.get('messages', [])

        for message in messages:
            m_data = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = m_data.get('payload', {})

            # パートに添付ファイルがあるか確認
            parts = payload.get('parts', [])
            for part in parts:
                filename = part.get("filename")
                body = part.get("body", {})
                attachment_id = body.get("attachmentId")

                if filename and attachment_id:
                    res = service.users().messages().attachments().get(
                        userId='me',
                        messageId=message['id'],
                        id=attachment_id
                    ).execute()
                    data = res.get('data')
                    if data:
                        file_data = base64_decode_file(data)
                        os.makedirs(save_folder, exist_ok=True)
                        filepath = os.path.join(save_folder, filename)
                        with open(filepath, 'wb') as f:
                            f.write(file_data)
                        print(f"保存済み: {filepath}")

def run_save_attachments(settings, retries=3, delay=5):
    import time
    attempt = 0
    while attempt < retries:
        print(f"{attempt + 1}回目の実行中...")
        save_attachments_from_email(settings)

        # 保存チェック
        saved_files = []
        for subject, save_folder in settings:
            if os.path.exists(save_folder):
                saved_files.extend(os.listdir(save_folder))

        if saved_files:
            print("保存されたファイル:", saved_files)
            break
        else:
            print("ファイルが保存されていません。再試行します...")
            time.sleep(delay)
            attempt += 1

    if attempt == retries:
        print("指定回数再試行してもファイルが保存されませんでした。")
