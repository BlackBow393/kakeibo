import win32com.client
import os

def save_attachments_from_email(settings):
    # Outlookオブジェクトを取得
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")

    # 受信トレイを取得
    inbox = namespace.GetDefaultFolder(6)  # 受信トレイ
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)  # 新しい順に並べ替え

    # 設定に基づいてメールを処理
    for msg in messages:
        if msg.UnRead:  # 未読のメールのみ処理
            # 設定に基づいて処理
            for subject, save_folder in settings:
                if subject in msg.Subject:  # 件名が一致した場合
                    # 添付ファイルの処理
                    if msg.Attachments.Count > 0:
                        for attachment in msg.Attachments:
                            attachment_name = attachment.FileName
                            attachment_path = os.path.join(save_folder, attachment_name)

                            # 添付ファイルを指定したパスに保存
                            attachment.SaveAsFile(attachment_path)
                            print(f"添付ファイル '{attachment_name}' を保存しました: {attachment_path}")
                    
                    # メールを既読にする（必要に応じて）
                    msg.UnRead = False
