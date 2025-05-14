from load_email_settings import load_email_settings
from save_attachments import save_attachments_from_email, run_save_attachments  # run_save_attachmentsもインポート
import os

# main.py が実行されるディレクトリを基準に相対パスで Excel ファイルを探す
current_dir = os.path.dirname(__file__)

# 相対パスで '受信設定ファイル_ver.1.0.0.xlsx' を探す
excel_file = os.path.join(current_dir, '受信設定ファイル_ver.1.0.0.xlsx')

# Excel ファイルが存在するか確認
if os.path.exists(excel_file):
    # 設定を読み込む
    settings = load_email_settings(excel_file)
    
    # 添付ファイルの保存処理を再試行機能付きで実行
    run_save_attachments(settings)
else:
    print(f"エラー: {excel_file} が見つかりません。ファイルが正しい場所にあることを確認してください。")
