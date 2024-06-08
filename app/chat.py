import json
import os
from os.path import dirname, join

import openai
from dotenv import find_dotenv, load_dotenv
from txt_to_json import txt_to_json


def chat(text) -> str:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(verbose=True, dotenv_path=dotenv_path)
    OPENAI_APIKEY = os.getenv("API_KEY")
    openai.api_key = OPENAI_APIKEY


    result = openai.chat.completions.create(
        model='gpt-4o',
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": """
あなたは面接担当の人事責任者です。次に送る文章を分析して、一つの項目につき20点で合計100点満点で点数化してください。出力形式は以下の形式を使用してください。また、どの部分がだめだったか、どのようにすればもっと良くなるかの理由を明示してください。whisperでテキスト変換しているため、そこも考慮してください。

# 出力形式（json）
{
    "evaluation1": {
        "score": xx,
        "reason": "評価理由"
    },
    "evaluation2": {
        "score": xx,
        "reason": "評価理由"
    },
    "evaluation3": {
        "score": xx,
        "reason": "評価理由"
    },
    "evaluation4": {
        "score": xx,
        "reason": "評価理由"
    },
    "evaluation5": {
        "score": xx,
        "reason": "評価理由"
    }
}

# 評価項目:

1. 口癖:
   - 無意識の発声: 「えー」や「あのー」といった無意識の発声が頻繁に見られるか。
   - 語尾: 語尾を「～ですかね」といったような癖があるか。
   - 話し始めの癖: 話し始めに特定のフレーズ（例：「まあ」、「とにかく」）を使う傾向があるか。

2. 一人称の統一:
   - 一貫性: 一人称が一貫しているか。「私」、「僕」、「俺」などが混在していないか。
   - 適切な一人称: 「私」を使用しているか。特にビジネスの場面では「私」が望ましい。

3. 敬語の使い方:
   - 二重敬語の回避: 二重敬語を使用していないか（例：「おっしゃられる」）。
   - 尊敬語、謙譲語、丁寧語の使い分け: 尊敬語（例：「おっしゃる」）、謙譲語（例：「申す」）、丁寧語（例：「です」、「ます」）を正しく使い分けているか。
   - 「御社」と「貴社」の使い分け: 面接時に「御社」（口語）と「貴社」（書面）の使い分けが適切か。

4. 論理性:
   - 結論から話す: 話の結論を先に述べ、その後に詳細や根拠を説明しているか。
   - 裏付ける根拠やエピソード: 主張を裏付ける具体的な根拠やエピソードを提供しているか。

5. 言葉の使い方:
   - 具体的な表現: 抽象的な言い方を避け、具体的な言葉を使っているか（例：「こちらの件」→「このプロジェクト」）。
   - 明確な表現: 肯定や否定のどちらにも受け取れる言葉を使っていないか（例：「大丈夫」→「問題ありません」）。
   - 適切な表現: 「こちら」、「あちら」などの曖昧な言葉を使わずに、具体的な対象を明確に述べているか（例：「こちらになります」→「この書類です」）。
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

