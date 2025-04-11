# perplexity_client.py
import os
import json
import requests

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
api_key = os.environ.get("PERPLEXITY_API_KEY")
model_name = "sonar-pro"

def fetch_latest_articles(category: str) -> dict:
    """
    指定されたカテゴリ ("news" または "tech") の最新記事上位3件を取得する関数。
    
    引数:
      category: "news" または "tech"
        - "news" → derivedCategory = "ニュース"
        - "tech" → derivedCategory = "技術記事"
    
    プロンプトでは、Google検索を用いて最新の {derivedCategory} 記事上位3件を取得し、各記事について
    タイトル(title)、要約された内容(content)、URL(url) を JSON 形式で出力するように指示します。
    
    出力例の JSON 形式:
    {
      "{derivedCategory}": {
         "1st": { "title": "string", "content": "string", "url": "string" },
         "2st": { "title": "string", "content": "string", "url": "string" },
         "3st": { "title": "string", "content": "string", "url": "string" }
      }
    }
    """
    if category.lower() == "news":
        derivedCategory = "ニュース"
    elif category.lower() == "tech":
        derivedCategory = "技術記事"

    system_prompt = f"""貴方はAIに関する専門家です。過去24時間以内に投稿されたAIに関する最新情報を収集し、簡潔に教えてください。"""

    prompt = f"""
    過去24時間にweb上に投稿されたAIに関する{derivedCategory}の中から、専門家の視点で特に重要だと考えられるものを3つ選び、それぞれの{derivedCategory}のタイトル、{derivedCategory}を簡潔に要約した内容、URL1個を教えてください。
    なお、情報源に指定は無いですが、出力は全て日本語で行ってください。

    注意点として、出力は以下に示すJSON形式に従ってください。 
    選択した3つの{derivedCategory}は、それぞれ「1st」、「2nd」、「3rd」として格納してください。
    なお、{derivedCategory}のタイトルは「title」、{derivedCategory}を簡潔に要約した内容は「content」、URLは「url」というキーを使ってください。
    また、以下に指定するjson形式以外の文字列は、絶対に出力しないでください。

    {{{{
      "{category}": {{
        "1st": {{
          "title": "string",
          "content": "string",
          "url": "string"
        }},
        "2nd": {{
          "title": "string",
          "content": "string",
          "url": "string"
        }},
        "3rd": {{
          "title": "string",
          "content": "string",
          "url": "string"
        }}
      }}
    }}}}"""

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        # "response_format": {},
        "web_search_options": {"search_context_size": "high"}
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.request("POST", PERPLEXITY_API_URL, json=payload, headers=headers)
    body = json.loads(response.text)
    output = body["choices"][0]["message"]["content"]
    
    return output
