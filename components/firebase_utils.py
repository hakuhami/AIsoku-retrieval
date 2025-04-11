import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# def init_firebase():
#     cred_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")
#     if not firebase_admin._apps:
#         cred = credentials.Certificate(cred_path)
#         firebase_admin.initialize_app(cred)
#     return firestore.client()

def init_firebase():
    cred_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")    
    if not firebase_admin._apps:
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

# Firestore クライアント
db = init_firebase()
