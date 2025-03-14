import requests

from fastapi import FastAPI, Response
from config import settings

app = FastAPI()


@app.get('/')
def home():
    return {"Chat": "Bot"}


@app.get('/ask')
def ask(prompt: str):
    # url = 'http://ollama:11434/api/generate'
    # url = "http://localhost:11434/api/generate"
    url = settings.ollama_url
    print(url)
    res = requests.post(url, json={
        "prompt": prompt,
        "stream": False,
        "model": "llama3.2"
    })

    return Response(content=res.text, media_type="application/json")
