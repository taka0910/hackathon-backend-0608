import json
import os
from os.path import dirname, join

import openai
from dotenv import find_dotenv, load_dotenv
from txt_to_json import txt_to_json


def summary(text) -> str:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(verbose=True, dotenv_path=dotenv_path)

    OPENAI_APIKEY = os.getenv("API_KEY")
    openai.api_key = OPENAI_APIKEY


    result = openai.chat.completions.create(
        model='gpt-4o',
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": 
             """
次の日本語のフィードバックを要約してjson形式で出力してください。重要なポイントと改善点を中心に、文章で100~200字程度で簡潔にまとめてください。
# 出力形式例
{
  "reason": "あなたは、～～の部分に癖があるので修正していく必要があります。また、～～の部分はとても良いと思いますので、今後も磨いていきましょう。"
}
           """},
            {"role": "user", "content": text},
        ]
    )
    response_text = result.choices[0].message.content
    print(response_text)

    try:
        response_json = json.loads(response_text)
        return response_json
    except json.JSONDecodeError as e:
        print("Error: Response is not in JSON format")
        print("Details:", e)
        return txt_to_json(response_text)

