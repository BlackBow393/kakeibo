import time
from load_email_settings import load_email_settings
from save_attachments import run_save_attachments
import os

def main_loop(interval_minutes=60):
    current_dir = os.path.dirname(__file__)
    excel_file = os.path.join(current_dir, '受信設定ファイル_ver.1.0.0.xlsx')

    if not os.path.exists(excel_file):
        print(f"エラー: {excel_file} が見つかりません。ファイルが正しい場所にあることを確認してください。")
        return

    settings = load_email_settings(excel_file)

    while True:
        try:
            print("メール確認・添付ファイル処理を実行中...")
            run_save_attachments(settings)
        except Exception as e:
            print(f"エラーが発生しました: {e}")
        print(f"{interval_minutes} 分後に再実行します...")
        time.sleep(interval_minutes * 60)

if __name__ == '__main__':
    main_loop()
