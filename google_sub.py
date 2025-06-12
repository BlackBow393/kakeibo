from google.cloud import pubsub_v1
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import json
from load_email_settings import load_email_settings
from save_attachments import run_save_attachments

# プロジェクトIDとサブスクリプションID
PROJECT_ID = "turing-energy-462700-m1"
SUBSCRIPTION_ID = "t93_gmail_push_topic-sub"

# パス生成
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

# 設定ファイルのパス
current_dir = os.path.dirname(__file__)
excel_file = os.path.join(current_dir, '受信設定ファイル_ver.1.0.0.xlsx')
token_file = os.path.join(current_dir, 'token.json')

def callback(message):
    print(f"\n📩 Received message: {message.data.decode('utf-8')}")
    
    message_json = json.loads(message.data.decode('utf-8'))
    history_id = message_json.get("historyId")

    if not history_id:
        print("⚠️ historyId が通知に含まれていません。")
        message.ack()
        return

    # Gmail API 認証
    creds = Credentials.from_authorized_user_file(token_file, ['https://mail.google.com/'])
    service = build('gmail', 'v1', credentials=creds)

    try:
        # 新しく追加されたメッセージ一覧を取得
        history_response = service.users().history().list(
            userId='me',
            startHistoryId=history_id,
            historyTypes=['messageAdded']
        ).execute()

        print(f"🔍 Gmail history fetched: {history_response.get('history', [])}")

        if 'history' in history_response:
            for history in history_response['history']:
                for msg in history.get('messages', []):
                    msg_id = msg['id']
                    print(f"📨 New message ID: {msg_id}")

                    # ここでメッセージ内容を取得して添付ファイル保存処理へ
                    if os.path.exists(excel_file):
                        settings = load_email_settings(excel_file)
                        run_save_attachments(settings, message_id=msg_id, service=service)
                    else:
                        print("⚠️ 設定ファイルが見つかりません。")
    except Exception as e:
        print(f"❌ エラー: {e}")

    message.ack()  # 正常に処理されたことを通知

def main():
    print(f"🔔 Listening for Gmail notifications on: {subscription_path}")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        print("⛔ 停止しました。")

if __name__ == "__main__":
    main()
