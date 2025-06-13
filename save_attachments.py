from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
import os
import time

# base64デコード関数
def base64_decode_file(data):
    return base64.urlsafe_b64decode(data.encode('UTF-8'))

def save_attachments_from_message_id(settings, message_id, service):
    m_data = service.users().messages().get(userId='me', id=message_id).execute()
    payload = m_data.get('payload', {})

    parts = payload.get('parts', [])
    for part in parts:
        filename = part.get("filename")
        body = part.get("body", {})
        attachment_id = body.get("attachmentId")

        if filename and attachment_id:
            res = service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=attachment_id
            ).execute()
            data = res.get('data')
            if data:
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                for subject, save_folder in settings:
                    os.makedirs(save_folder, exist_ok=True)
                    filepath = os.path.join(save_folder, filename)
                    with open(filepath, 'wb') as f:
                        f.write(file_data)
                    print(f"📎 添付ファイルを保存: {filepath}")

# -----------------------------------------------------------------------------
# 【1】件名に一致するメールすべてから添付ファイルを保存（バッチ・手動処理用）
# -----------------------------------------------------------------------------
def save_attachments_from_email(settings):
    creds = Credentials.from_authorized_user_file('token.json', ['https://mail.google.com/'])
    service = build('gmail', 'v1', credentials=creds)

    for subject, save_folder in settings:
        query = f"subject:{subject}"
        messages_response = service.users().messages().list(userId='me', q=query).execute()
        messages = messages_response.get('messages', [])

        for message in messages:
            m_data = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = m_data.get('payload', {})

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
                        print(f"✅ 保存済み: {filepath}")

# -----------------------------------------------------------------------------
# 【2】Pub/Sub通知で受け取った特定の1通のメールから添付ファイルを保存（通知処理用）
# -----------------------------------------------------------------------------
def save_attachments_by_msg_id(settings, message_id, service):
    m_data = service.users().messages().get(userId='me', id=message_id).execute()
    payload = m_data.get('payload', {})
    headers = payload.get("headers", [])
    subject = ""

    # 件名を抽出
    for header in headers:
        if header['name'].lower() == 'subject':
            subject = header['value']
            break

    if not subject:
        print("⚠️ 件名が取得できませんでした。スキップします。")
        return

    for setting_subject, save_folder in settings:
        if setting_subject in subject:
            print(f"📂 件名「{subject}」にマッチ: {setting_subject}")
            parts = payload.get('parts', [])
            for part in parts:
                filename = part.get("filename")
                body = part.get("body", {})
                attachment_id = body.get("attachmentId")

                if filename and attachment_id:
                    res = service.users().messages().attachments().get(
                        userId='me',
                        messageId=message_id,
                        id=attachment_id
                    ).execute()
                    data = res.get('data')
                    if data:
                        file_data = base64_decode_file(data)
                        os.makedirs(save_folder, exist_ok=True)
                        filepath = os.path.join(save_folder, filename)
                        with open(filepath, 'wb') as f:
                            f.write(file_data)
                        print(f"✅ 添付ファイル保存: {filepath}")
            break  # 一致したら1件で終了

# -----------------------------------------------------------------------------
# 【3】再試行付きでバッチ処理用関数を実行するユーティリティ関数
# -----------------------------------------------------------------------------
def run_save_attachments(settings, message_id=None, service=None, retries=3, delay=5):
    import time
    attempt = 0
    while attempt < retries:
        print(f"{attempt + 1}回目の実行中...")

        if message_id and service:
            from save_attachments import save_attachments_from_message_id
            save_attachments_from_message_id(settings, message_id, service)
        else:
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

