import pandas as pd

def load_email_settings(excel_file):
    # Excelファイルを読み込む
    df = pd.read_excel(excel_file, sheet_name="設定", engine='openpyxl')
    
    # 件名と保存先パスの設定を読み込む（「設定テーブル」シートから）
    settings = []
    for index, row in df.iterrows():
        subject = row.get("件名")
        save_path = row.get("保存先パス")
        
        # もし件名と保存先パスが両方とも存在すれば設定リストに追加
        if subject and save_path:
            settings.append((subject, save_path))
    
    return settings
