# openai_client.py
import os
import json
import openai

# OpenAI の API キーは環境変数から取得する
openai.api_key = os.environ.get("OPENAI_API_KEY")

def fetch_latest_articles(category: str) -> dict:
    """
    OpenAI GPT-4o を呼び出し、指定カテゴリの最新記事上位3件を取得する。
    出力例（構造化された JSON）：
      {
         "1st": { "title": "記事タイトル1", "content": "要約1", "url": "https://..." },
         "2st": { "title": "記事タイトル2", "content": "要約2", "url": "https://..." },
         "3st": { "title": "記事タイトル3", "content": "要約3", "url": "https://..." }
      }
    """
    system_message = (
        f"You are a web search assistant. Using your integrated web search function, fetch the top 3 latest articles for the category '{category}'. "
        "Return a JSON object with keys \"1st\", \"2st\", \"3st\" where each value is an object containing 'title', 'content', and 'url'. "
        "Output only the JSON without any extra text."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
            ],
            temperature=0.0,
            max_tokens=500,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to call OpenAI API: {e}")

    output_text = response.choices[0].message.content.strip()
    try:
        data = json.loads(output_text)
    except Exception as e:
        raise ValueError(f"Error parsing JSON from GPT-4o output: {e}\nOutput was: {output_text}")
    return data
