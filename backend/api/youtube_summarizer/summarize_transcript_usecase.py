from fastapi import HTTPException
from .summarize_transcript import YoutubeSummarizer


class SummarizeTranscriptUsecase:
    @staticmethod
    def execute(transcript: str, ollama_base_url) -> str:
        try:
            summarizer = YoutubeSummarizer(ollama_base_url)
            summary = summarizer.summarize_transcripts(transcript)
            return summary
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
