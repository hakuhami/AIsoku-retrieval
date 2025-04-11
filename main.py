# # main.py
# from components.update_firestore import shift_updates, update_latest_articles

# from dotenv import load_dotenv

# load_dotenv()

# def main():
#     try:
#         print("シフト処理を開始します...")
#         shift_updates()
#         print("最新記事を GPT-4o API から取得中...")
#         update_latest_articles()
#         print("更新が完了しました。")
#     except Exception as e:
#         print("エラーが発生しました:", e)

# if __name__ == "__main__":
#     main()



# apiが動いているかのテスト
import json
from dotenv import load_dotenv

load_dotenv()

from components.perplexity_client import fetch_latest_articles

def main():
    try:
        print("最新ニュース記事を API から取得中...")
        
        # fetch_latest_articles("news")の結果をターミナルに出力
        print("\n=== AIに関する最新ニュース ===")
        news_result = fetch_latest_articles("news")
        # print(json.dumps(news_result, ensure_ascii=False, indent=2))
        print(news_result)
        print("=====================================")
        
    except Exception as e:
        print("エラーが発生しました:", e)

if __name__ == "__main__":
    main()
