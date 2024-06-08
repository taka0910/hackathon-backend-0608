import os
from io import BytesIO
from os.path import dirname, join

import openai
from dotenv import find_dotenv, load_dotenv


def voice_to_text(url):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(verbose=True, dotenv_path=dotenv_path)
    OPENAI_APIKEY = os.getenv("API_KEY")
    openai.api_key = OPENAI_APIKEY

    audio = open(url, "rb")
    transcript = openai.audio.transcriptions.create(
        file = audio,
        model = 'whisper-1',
        language='ja')
    return transcript.text