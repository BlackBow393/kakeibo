from load_email_settings import load_email_settings
from save_attachments import run_save_attachments
import os

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(__file__)

# Excel 設定ファイルのパス
excel_file = os.path.join(current_dir, '受信設定ファイル_ver.1.0.0.xlsx')

# Excelファイルが存在するかをチェック
if os.path.exists(excel_file):
    # 件名と保存先ディレクトリを読み込み
    settings = load_email_settings(excel_file)
    
    # Gmail API を使って添付ファイルを保存（再試行あり）
    run_save_attachments(settings)
else:
    print(f"エラー: {excel_file} が見つかりません。パスを確認してください。")
