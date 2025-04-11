from components.firebase_utils import db
from components.perplexity_client import fetch_latest_articles
import json

def shift_updates():
    """
    Firestore の更新データをシフトする処理:
      - v5 のデータを削除
      - v4 のデータを v5 にコピー
      - v3 のデータを v4 にコピー
      - v2 のデータを v3 にコピー
      - v1 のデータを v2 にコピー
    ※各更新はコレクション名として扱い、各コレクションには "news" と "tech" の2つのドキュメントが存在する前提。
    """
    doc_names = ["news", "tech"]
    
    # v5 のデータを削除
    for doc_name in doc_names:
        v5_ref = db.collection("v5").document(doc_name)
        v5_doc = v5_ref.get()
        if v5_doc.exists:
            v5_ref.delete()
    
    # データをシフト処理（v4→v5, v3→v4, v2→v3, v1→v2）
    for i in range(4, 0, -1):
        src = f"v{i}"
        dst = f"v{i+1}"
        
        for doc_name in doc_names:
            src_ref = db.collection(src).document(doc_name)
            src_doc = src_ref.get()
            if src_doc.exists:
                # データを取得してコピー先に保存
                data = src_doc.to_dict()
                db.collection(dst).document(doc_name).set(data)

def update_latest_articles():
    """
    LLM API を利用して、"news" と "tech" の最新記事上位3件を取得し、
    Firestore の "v1" コレクションの対応するドキュメントに格納する処理
    """
    # news記事を取得
    news_response = fetch_latest_articles("news")
    news_response = json.loads(news_response)
    # articlesキーの値を取得
    news_articles = news_response["articles"]
    db.collection("v1").document("news").set(news_articles)
    
    # tech記事も同様に処理
    tech_response = fetch_latest_articles("tech")
    tech_response = json.loads(tech_response)        
    # articlesキーの値を取得
    tech_articles = tech_response["articles"]
    db.collection("v1").document("tech").set(tech_articles)    