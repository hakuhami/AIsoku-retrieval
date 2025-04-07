# firebase_utils.py
import os
import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    # サービスアカウントキーのパスを環境変数 FIREBASE_SERVICE_ACCOUNT_PATH から取得
    cred_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH", "path/to/your/serviceAccountKey.json")
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()

# Firestore クライアント
db = init_firebase()
