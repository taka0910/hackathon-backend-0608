import json
import os
from os.path import dirname, join

import openai
from dotenv import find_dotenv, load_dotenv
from txt_to_json import txt_to_json


def es_feedback(text) -> str:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(verbose=True, dotenv_path=dotenv_path)
    OPENAI_APIKEY = os.getenv("API_KEY")
    openai.api_key = OPENAI_APIKEY
    result = openai.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": """
次に送るエントリーシートの文章を添削してください。出力形式に従って必ず複数出力してください。

# 注意事項
・添削する部分がない場合や、関係のない文章であった場合は添削なしとしてください。
・出力形式の添削前文章は、絶対に一文にしてください。同じような理由でも分けて出力してください。
・関係のない文章は絶対に何も出力しないでください。

# 出力形式（json形式）

{
"text1": {"添削前文章":"~~~","添削後文章":"~~~","添削理由":"~~~"},
"text2": {"添削前文章":"~~~","添削後文章":"~~~","添削理由":"~~~"},
"textn": {"添削前文章":"~~~","添削後文章":"~~~","添削理由":"~~~"},
}

# 評価項目:

1.文章の構成:
序論、本論、結論の明確さ: 文章が明確な序論、本論、結論の構成を持っているか。
段落分けの適切さ: 各段落が一つのテーマに集中しており、適切に段落分けされているか。

2.内容の具体性:
具体例の使用: 主張を裏付ける具体的なエピソードやデータが使用されているか。
詳細な説明: 抽象的な表現ではなく、具体的な言葉を用いて説明されているか。

3.論理性:
一貫した論理: 文章全体が一貫した論理に基づいて書かれているか。
論理の飛躍がないか: 論理の飛躍や矛盾がないか。

4.文法と語法:
正しい文法の使用: 文法的な誤りがないか。
適切な語彙の使用: 語彙の選択が適切であり、意味が明確に伝わるか。

5.敬語の使い方:
敬語の正確な使用: 敬語、謙譲語、丁寧語が正しく使い分けられているか。
二重敬語の回避: 二重敬語が使用されていないか。

6.一人称の統一:
一貫した一人称: 一人称が一貫しているか。「私」、「僕」、「俺」などが混在していないか。
適切な一人称: ビジネス文書として「私」が使用されているか。

7.言葉の使い方:
具体的な表現: 抽象的な言い方を避け、具体的な言葉を使っているか。
明確な表現: 肯定や否定のどちらにも受け取れる言葉を使っていないか。
適切な表現: 「こちら」、「あちら」などの曖昧な言葉を使わずに、具体的な対象を明確に述べているか。

8.説得力:
強い主張: 説得力のある主張が行われているか。
根拠の提示: 主張を裏付ける根拠やエピソードが適切に提示されているか。

9.読みやすさ:
文章の流れ: 文章がスムーズに読み進められるか。
簡潔さ: 冗長な表現を避け、簡潔に書かれているか。
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
        print("json形式が正しくないのでjsonに変換する関数を通します。")
        return txt_to_json(response_text)
