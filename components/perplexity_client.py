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
        system_prompt = f"""貴方はAIに関する専門家です。貴方には、毎日AIに関する最新情報を速報として、日本語で詳細に提供するタスクが与えられています。"""

        prompt = f"""
        過去24時間以内にweb上に投稿されているAIに関する最新のニュースを調査し、その中から専門家の視点で特に重要だと考えられるものを3つ選び、それぞれのニュースのタイトル、ニュースを簡潔に要約した内容、URL1個を教えてください。
        なお、情報源に指定は無いですが、出力は全て日本語で行ってください。

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
        system_prompt = f"""貴方はAI関係の開発に携わるエンジニア兼リサーチャーです。貴方には、自分と同じ立場の人向けに、毎日AIに関する最新の技術記事を日本語で詳細に解説するタスクが与えられています。"""

        prompt = f"""
        現時点でweb上に投稿されているAIに関する最新の日本語の技術記事を調査し、その中から技術的に特に重要だと考えられるものを3つ選び、それぞれのページのタイトル、ページの内容を簡潔に要約した内容、URL1個を教えてください。
        なお、情報源は貴方がAI関係の開発を行う際に実際に閲覧するページとし、全て日本語で記載されたものを参照し、出力は全て日本語で行ってください。

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
