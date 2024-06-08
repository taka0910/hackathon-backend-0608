import json
import os
from os.path import dirname, join

import openai
from dotenv import find_dotenv, load_dotenv


def txt_to_json(text) -> str:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(verbose=True, dotenv_path=dotenv_path)

    OPENAI_APIKEY = os.getenv("API_KEY")
    openai.api_key = OPENAI_APIKEY


    result = openai.chat.completions.create(
        model='gpt-4o',
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": """
以下はjson形式に変換できなかった形式になります。正しいjson形式に変換して出力してください。
# 出力形式（json）
{
"text1": {"添削前文章":"~~~","添削語文章":"~~~","添削理由":"~~~"},
"text2": {"添削前文章":"~~~","添削語文章":"~~~","添削理由":"~~~"},
"textn": {"添削前文章":"~~~","添削語文章":"~~~","添削理由":"~~~"},
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
        return None
    
