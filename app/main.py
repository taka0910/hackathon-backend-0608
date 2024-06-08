import json
import os
from concurrent.futures import ProcessPoolExecutor
from os.path import dirname, join
from typing import List, Union

import aiofiles
import openai
import requests
from chat import chat
from dotenv import find_dotenv, load_dotenv
from es_feedback import es_feedback
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from summary import summary
from whisper import voice_to_text

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(verbose=True, dotenv_path=dotenv_path)
OPENAI_APIKEY = os.getenv("API_KEY")
openai.api_key = OPENAI_APIKEY


app = FastAPI()

origins = [
    "http://localhost:3000",  # Reactのサーバーを許可する
    "https://hackathon-wine-mu.vercel.app/"  # 追加するオリジン
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 許可するオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return { dotenv_path : OPENAI_APIKEY}

@app.post("/upload/")
async def upload_audio(files: List[UploadFile] = File(...)):
    results = []
    video_list = []
    for file in files:
        async with aiofiles.open(f'tmp/{file.filename}', 'wb') as out_file:
            content = await file.read()  # Read file content
            await out_file.write(content)
        video_list.append(f"tmp/{file.filename}")
    
    # ProcessPoolExecutorを使用して複数のプロセスで処理
    with ProcessPoolExecutor() as executor:
        text_list = list(executor.map(voice_to_text, video_list))
    with ProcessPoolExecutor() as executor:
        feedback_list = list(executor.map(chat, text_list))
    results = [{"filename": files[i].filename, "input_text": text_list[i], "response": feedback_list[i]} for i in range(len(video_list))]

    # ここから添削まとめの指示
    reasons = []
    for item in results:
        response = item['response']
        for evaluation in response.values():
            reasons.append(evaluation['reason'])

    # 関数を通す
    summary_data = summary(str(reasons))
    # 結果の出力
    results.append(summary_data)
    return json.dumps(results, ensure_ascii=False, indent=4)





@app.post("/es_feedback/")
async def upload_text(texts: List[str] = Form(...)):
    # ProcessPoolExecutorを使用して複数のプロセスで処理
    with ProcessPoolExecutor() as executor:
        feedback_list = list(executor.map(es_feedback, texts))

    results = [{"input_text": texts[i], "response": feedback_list[i]} for i in range(len(texts))]
    return json.dumps(results, ensure_ascii=False, indent=4)