from components.firebase_utils import db
from components.perplexity_client import fetch_latest_articles
import json

def shift_updates():
    """
    Firestore の更新データをシフトする処理:
      - v1 のデータを v2 にコピー
      - v2 のデータを v3 にコピー
      - v3 のデータを v4 にコピー
      - v4 のデータを v5 にコピー
      - v5 のデータは削除する
    ※各更新はコレクション名として扱い、各コレクションには "news" と "tech" の2つのドキュメントが存在する前提です。
    """
    # ドキュメント名のリスト
    doc_names = ["news", "tech"]
    
    # 各ドキュメントごとにシフト処理を行う
    for doc_name in doc_names:
        for i in range(4, 0, -1):
            src = f"v{i}"
            dst = f"v{i+1}"
            src_ref = db.collection(src).document(doc_name)
            src_doc = src_ref.get()
            if src_doc.exists:
                db.collection(dst).document(doc_name).set(src_doc.to_dict())
    
    # v5 のデータを削除
    for doc_name in doc_names:
        v5_ref = db.collection("v5").document(doc_name)
        if v5_ref.get().exists:
            v5_ref.delete()

def update_latest_articles():
    """
    Perplexity API を利用して、"news" と "tech" の最新記事上位3件を取得し、
    Firestore の "v1" コレクションの対応するドキュメントに格納する処理
    """
    # news記事を取得
    news_response = fetch_latest_articles("news")
    
    news_response = json.loads(news_response)
    # articlesキーの値を取得
    news_articles = news_response["articles"]
    # "v1"コレクションの"news"ドキュメントに保存
    db.collection("v1").document("news").set(news_articles)
    
    # # strが返って来るため、JSONとしてパース
    # if isinstance(news_response, str):        
    #     news_response = json.loads(news_response)
    #     # articlesキーの値を取得
    #     news_articles = news_response["articles"]
    #     # "v1"コレクションの"news"ドキュメントに保存
    #     db.collection("v1").document("news").set(news_articles)
    
    # # 万が一辞書型の場合の処理
    # if isinstance(news_response, dict):
    #     if "articles" in news_response:
    #         # articlesキーの値を取得
    #         news_articles = news_response["articles"]
    #         # "v1"コレクションの"news"ドキュメントに保存
    #         db.collection("v1").document("news").set(news_articles)
    #     else:
    #         db.collection("v1").document("news").set(news_response)
    
    # tech記事も同様に処理
    tech_response = fetch_latest_articles("tech")
    
    tech_response = json.loads(tech_response)        
    # articlesキーの値を取得
    tech_articles = tech_response["articles"]
    # "v1"コレクションの"tech"ドキュメントに保存
    db.collection("v1").document("tech").set(tech_articles)
    
    # # 文字列の場合はJSONとしてパース
    # if isinstance(tech_response, str):
    #     tech_response = json.loads(tech_response)        
    #     # articlesキーの値を取得
    #     tech_articles = tech_response["articles"]
    #     # "v1"コレクションの"tech"ドキュメントに保存
    #     db.collection("v1").document("tech").set(tech_articles)
    
    # # 辞書型の場合、通常の処理を続行
    # if isinstance(tech_response, dict):
    #     if "articles" in tech_response:
    #         # articlesキーの値を取得
    #         tech_articles = tech_response["articles"]
    #         # "v1"コレクションの"tech"ドキュメントに保存
    #         db.collection("v1").document("tech").set(tech_articles)
    #         print(f"techデータを保存しました: {tech_articles.keys()}")
    #     else:
    #         # articlesキーがない場合は、データ全体を保存
    #         db.collection("v1").document("tech").set(tech_response)
    #         print(f"techデータを代替形式で保存しました: {tech_response.keys()}")
    