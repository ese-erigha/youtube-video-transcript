import requests

from fastapi import FastAPI, Response
from config import settings
from youtube_summarizer.get_transcripts_usecase import GetTranscriptsUsecase
from youtube_summarizer.summarize_transcript_usecase import SummarizeTranscriptUsecase
from youtube_summarizer.transcript_response_dto import GetTranscriptsResponseDto, \
    SummarizeTranscriptResponseDto
from youtube_summarizer.summarize_transcript import YoutubeSummarizer

app = FastAPI()


@app.get('/')
def home():
    return {"Chat": "Bot"}


@app.get('/ask')
def ask(prompt: str):
    url = settings.ollama_base_url + settings.ollama_generate_path
    print(url)
    res = requests.post(url, json={
        "prompt": prompt,
        "stream": False,
        "model": "llama3.2"
    })

    return Response(content=res.text, media_type="application/json")


@app.get('/youtube/video/transcripts')
def get_youtube_video_transcripts(video_url: str) -> GetTranscriptsResponseDto:
    transcripts = GetTranscriptsUsecase.execute(video_url)
    return GetTranscriptsResponseDto(transcripts=transcripts)


@app.get('/youtube/video/transcript/summarize')
def summarize_video_transcript(transcript: str) -> SummarizeTranscriptResponseDto:
    summary = SummarizeTranscriptUsecase.execute(transcript, settings.ollama_base_url)
    return SummarizeTranscriptResponseDto(summary=summary)


@app.get('/youtube/video/summarize')
def summarize_video(video_url: str) -> dict[str, str]:
    youtube_summarizer = YoutubeSummarizer(settings.ollama_base_url)
    result = youtube_summarizer.summarize_video(video_url)
    return {"summary": result["summary"]["output_text"]}
