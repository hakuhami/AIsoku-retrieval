# gemini_client.py
import os
import requests

# Gemini API のエンドポイントと API キーは環境変数から取得
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# プロンプト作成と、構造化出力

def fetch_latest_articles(category: str) -> dict:
    """
    Gemini API を呼び出し、指定したカテゴリ ("news" または "tech") の最新記事上位3件を取得する。
    期待される出力例:
      {
        "1st": { "title": "...", "content": "...", "url": "..." },
        "2st": { ... },
        "3st": { ... }
      }
    """
    payload = {
        "model": "gemini-2.5-pro-exp-03-25",
        "prompt": f"Google検索で最新の{category}記事上位3件を取得し、各記事のタイトル、要約された内容、URLをJSON形式で出力してください.",
        "output_format": "structured"
    }
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
