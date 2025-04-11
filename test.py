# APIが動いているか、ローカルでテストするためのスクリプト

from dotenv import load_dotenv
load_dotenv()

# LLMを動かすコンポーネントをインポート
from components.perplexity_client import fetch_latest_articles

def main():
    try:
        print("\n=== 以下はLLMによる取得データ ===")
        
        news_result = fetch_latest_articles("news")
        print(news_result)
        
        # news_result = fetch_latest_articles("news")
        # print(news_result)
        
        print("=====================================")
        
    except Exception as e:
        print("エラーが発生しました:", e)

if __name__ == "__main__":
    main()