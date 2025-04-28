import os
import json
import requests
from pydantic import BaseModel, Field
from typing import Dict

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
api_key = os.environ.get("PERPLEXITY_API_KEY")
model_name = "sonar-pro"

class ArticleInfo(BaseModel):
    """個別の記事情報を表すモデル"""
    title: str = Field(..., description="記事のタイトル")
    content: str = Field(..., description="記事の要約内容")
    url: str = Field(..., description="記事のURL")

class RankedArticles(BaseModel):
    """1st, 2nd, 3rdの記事を格納するモデル"""
    first: ArticleInfo = Field(..., alias="1st")
    second: ArticleInfo = Field(..., alias="2nd")
    third: ArticleInfo = Field(..., alias="3rd")

class AnswerFormat(BaseModel):
    """APIレスポンスの最終形式"""
    articles: Dict[str, RankedArticles] = Field(..., description="カテゴリごとの記事データ")

def fetch_latest_articles(category: str):
    # ニュース記事を取得
    if category.lower() == "news":
        search_recency_filter = "day" # 過去24時間以内の情報を取得する
        system_prompt = f"""貴方はAIに関する専門家です。貴方には、毎日AIに関する最新情報を速報として、日本語で詳細に提供するタスクが与えられています。"""

        prompt = f"""
        過去24時間以内にweb上に投稿されているAIに関する最新のニュースを調査し、その中から専門家の視点で特に重要だと考えられるものを3つ選び、それぞれのニュースのタイトル、ニュースを簡潔に要約した内容、URL1個を教えてください。
        なお、情報源はなるべく1次情報に近い信憑性の高いもの（noteなど個人が執筆した記事やまとめサイトは含めない。）に限定してください。また、情報源は日本語または英語のものに限定し、出力は全て日本語で行ってください。

        注意点として、出力は以下に示すJSON形式に従ってください。
        選択した3つのニュースは、それぞれ「1st」、「2nd」、「3rd」として格納してください。
        なお、ニュースのタイトルは「title」、ニュースを簡潔に要約した内容は「content」、URLは「url」というキーを使ってください。

        {{{{
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
        }}}}"""
    
    # 技術記事を取得
    elif category.lower() == "tech":
        search_recency_filter = "week" # 過去1週間の情報を取得する
        
        system_prompt = f"""貴方はAIの研究開発における専門家です。貴方には、自分と同じAIの研究開発者向けに、毎日AIに関する最新の技術記事を日本語で詳細に解説するタスクが与えられています。"""

        prompt = f"""
        web上に投稿されているAIに関する最新の技術記事を調査し、その中からAIの研究開発者とってに特に重要だと考えられ、かつ可能な限り最新のものを3つ選び、それぞれのページのタイトル、ページの内容を詳しく説明した内容（要点を抑えて、明確に分かりやすく）、URL1個を教えてください。
        なお、情報源は技術的に粒度が高い内容とし、かつなるべく1次情報に近い信憑性の高いもの（具体的には、論文、企業の公式ドキュメント、企業のテックブログなど。noteなど個人が執筆した記事やまとめサイトは含めない。）に限定してください。また、情報源は日本語または英語のものに限定し、出力は全て日本語で行ってください。

        注意点として、出力は以下に示すJSON形式に従ってください。
        選択した3つのページは、それぞれ「1st」、「2nd」、「3rd」として格納してください。
        なお、ページのタイトルは「title」、ページを簡潔に要約した内容は「content」、URLは「url」というキーを使ってください。

        {{{{
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
        }}}}"""

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": AnswerFormat.model_json_schema()},
        },
        "web_search_options": {"search_context_size": "high"},
        "search_recency_filter": search_recency_filter
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.request("POST", PERPLEXITY_API_URL, json=payload, headers=headers)
    body = json.loads(response.text)
    output = body["choices"][0]["message"]["content"]
    
    return output
