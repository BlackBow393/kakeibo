from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def setup_watch():
    creds = Credentials.from_authorized_user_file('token.json', ['https://mail.google.com/'])
    service = build('gmail', 'v1', credentials=creds)

    # Gmail Push Notification の watch 呼び出し
    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/turing-energy-462700-m1/topics/t93_gmail_push_topic'
    }

    response = service.users().watch(userId='me', body=request).execute()
    print("Watch response:", response)

if __name__ == "__main__":
    setup_watch()
