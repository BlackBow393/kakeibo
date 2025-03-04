import win32com.client
import os
import time

def save_attachments_from_email(settings):
    # Outlookオブジェクトを取得
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")

    # 初期処理の遅延を追加（Outlookの起動待機）
    time.sleep(5)  # 5秒待機（必要に応じて調整）

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

                            # 添付ファイルが保存されるまで少し待機
                            wait_time = 3  # 3秒間待機（必要に応じて調整）
                            for _ in range(wait_time):
                                if os.path.exists(attachment_path):
                                    print(f"添付ファイルが正常に保存されました: {attachment_path}")
                                    break
                                time.sleep(1)  # 1秒待機して再確認

                            # 保存が確認できない場合はエラーメッセージを出力
                            if not os.path.exists(attachment_path):
                                print(f"添付ファイルの保存に失敗しました: {attachment_path}")
                                continue  # 再度実行する場合、ここで処理を継続

                    # メールを既読にする（必要に応じて）
                    msg.UnRead = False


# 保存されたか確認して、失敗した場合に再度実行
def run_save_attachments(settings, retries=3, delay=5):
    attempt = 0
    while attempt < retries:
        print(f"{attempt + 1}回目の実行中...")
        save_attachments_from_email(settings)
        
        # 添付ファイルが保存されているかを確認
        saved_files = []
        for subject, save_folder in settings:
            for filename in os.listdir(save_folder):
                saved_files.append(filename)
        
        # 保存されたファイルがあるかチェック
        if saved_files:
            print(f"保存されたファイル: {saved_files}")
            break
        else:
            print("添付ファイルが保存されていませんでした。再試行します。")
            attempt += 1
            time.sleep(delay)  # 再試行の前に待機

    if attempt == retries:
        print("指定した回数の再試行後もファイルが保存されませんでした。")
