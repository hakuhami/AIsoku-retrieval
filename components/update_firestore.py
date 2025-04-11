# update_firestore.py
from datetime import datetime
from firebase_utils import db
from components.perplexity_client import fetch_latest_articles

def shift_updates():
    """
    Firestore の更新データをシフトする処理:
      - v1 のデータを v2 にコピー
      - v2 のデータを v3 にコピー
      - v3 のデータを v4 にコピー
      - v4 のデータを v5 にコピー
      - v5 のデータは削除する
    ※各更新はコレクション名として扱い、各コレクションのドキュメント名は "data" とする前提です。
    """
    for i in range(4, 0, -1):
        src = f"v{i}"
        dst = f"v{i+1}"
        src_ref = db.collection(src).document("data")
        src_doc = src_ref.get()
        if src_doc.exists:
            db.collection(dst).document("data").set(src_doc.to_dict())
    # v5 のデータを削除
    v5_ref = db.collection("v5").document("data")
    if v5_ref.get().exists:
        v5_ref.delete()

def update_latest_articles():
    """
    Open AI API を利用して、"news" と "tech" の最新記事上位3件を取得し、Firestore の "v1" に格納する処理
    """
    news_data = fetch_latest_articles("news")
    tech_data = fetch_latest_articles("tech")
    
    update_data = {
        "news": news_data,   # 例: {"1st": {...}, "2st": {...}, "3st": {...}}
        "tech": tech_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # "v1" コレクションのドキュメント "data" に新データを保存
    db.collection("v1").document("data").set(update_data)
