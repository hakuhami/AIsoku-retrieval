# openai_client.py
import os
import json
from openai import OpenAI

# OpenAI の API キーは環境変数から取得
def get_openai_key():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key

model_name = "gpt-4o-2024-11-20"

def fetch_latest_articles(category: str):
    """
    指定されたカテゴリに基づき、OpenAI GPT-4o (モデル:"gpt-4o-search-preview") を利用して、
    最新の{derivedCategory}記事上位3件の情報を取得する関数です。
    
    引数:
      category: "news" または "tech"
      
    ※ "news" が指定された場合、{derivedCategory} は「ニュース」
       "tech" が指定された場合、{derivedCategory} は「技術記事」となります。
    
    Structured Output の JSON 形式:
    {
      "{derivedCategory}": {
        "1st": {
          "title": "string",
          "content": "string",
          "url": "string"
        },
        "2nd": { ... },
        "3rd": { ... }
      }
    }
    """
    # カテゴリに応じた表示用名称を設定
    if category.lower() == "news":
        derivedCategory = "ニュース"
    elif category.lower() == "tech":
        derivedCategory = "技術記事"
    else:
        raise ValueError("Invalid category. Use 'news' or 'tech'.")
      
    prompt = f"""貴方はAIに関する専門家です。
    私は日々AIに関する情報を収集しているのですが、AI技術の進歩は非常に早く、情報収集は非常に大変です。
    そこで、貴方には最新のAIに関する{derivedCategory}をweb上から収集し、私に簡潔に教えて欲しいです。
    具体的には、過去24時間以内にweb上に投稿されたAIに関する{derivedCategory}の中から、特に重要だと考えられるものを3つ選び、それぞれの{derivedCategory}のタイトル、{derivedCategory}を簡潔に要約した内容、URL1個を教えて欲しいです。 
    なお、情報源に指定は無いですが、出力は全て日本語で行ってください。

    注意点として、出力は以下に示すJSON形式に従ってください。 
    選択した3つの{derivedCategory}は、重要度の高い順に「1st」、「2st」、「3st」として格納してください。
    なお、{derivedCategory}のタイトルは「title」、{derivedCategory}を簡潔に要約した内容は「content」、URLは「url」というキーを使ってください。

    {{{{
      "{category}": {{
        "1st": {{
          "title": "string",
          "content": "string",
          "url": "string"
        }},
        "2st": {{
          "title": "string",
          "content": "string",
          "url": "string"
        }},
        "3st": {{
          "title": "string",
          "content": "string",
          "url": "string"
        }}
      }}
    }}}}"""
    
    # prompt = f"""貴方はAIに関する専門家です。過去24時間以内にweb上に投稿されたAIに関するニュースについて、詳細に教えてください。"""

    client = OpenAI(api_key=get_openai_key())
    # response = client.chat.completions.create(
    #     model=model_name,
    #     web_search_options={
    #         "search_context_size": "medium",
    #         "user_location": {
    #             "type": "approximate",
    #             "approximate": {
    #                 "country": "JP",
    #             },
    #         },
    #     },
    #     messages=[
    #         {"role": "system", "content": "あなたはAIに関する専門家です。"},
    #         {"role": "user", "content": prompt}
    #     ],
    #     # functions=[
    #     #     {
    #     #         "name": "get_latest_articles",
    #     #         "description": f"最新のAIに関する{derivedCategory}記事3件をjsonデータとして返します",
    #     #         "parameters": {
    #     #             "type": "object",
    #     #             "properties": {
    #     #                 f"{category}": {
    #     #                     "type": "object",
    #     #                     "properties": {
    #     #                         "1st": {
    #     #                             "type": "object",
    #     #                             "properties": {
    #     #                                 "title": {"type": "string"},
    #     #                                 "content": {"type": "string"},
    #     #                                 "url": {"type": "string"}
    #     #                             },
    #     #                             "required": ["title", "content", "url"]
    #     #                         },
    #     #                         "2nd": {
    #     #                             "type": "object",
    #     #                             "properties": {
    #     #                                 "title": {"type": "string"},
    #     #                                 "content": {"type": "string"},
    #     #                                 "url": {"type": "string"}
    #     #                             },
    #     #                             "required": ["title", "content", "url"]
    #     #                         },
    #     #                         "3rd": {
    #     #                             "type": "object",
    #     #                             "properties": {
    #     #                                 "title": {"type": "string"},
    #     #                                 "content": {"type": "string"},
    #     #                                 "url": {"type": "string"}
    #     #                             },
    #     #                             "required": ["title", "content", "url"]
    #     #                         }
    #     #                     },
    #     #                     "required": ["1st", "2nd", "3rd"]
    #     #                 }
    #     #             },
    #     #             "required": [f"{category}"]
    #     #         }
    #     #     }
    #     # ],
    #     # function_call={"name": "get_latest_articles"},
    #     temperature=0
    # )
    
    response = client.responses.create(
        model="gpt-4o-2024-11-20",
        tools=[{
            "type": "web_search_preview",
            "search_context_size": "high",
        }],
        input=prompt
    )
    
    # # Extract only the content generated by GPT from the response data
    # function_args = response.choices[0].message.function_call.arguments
    # return json.loads(function_args)
    
    print(prompt)
    print("=====================================")
    
    return response.output[1].content[0].text