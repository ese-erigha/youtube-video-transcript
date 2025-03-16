from pydantic import BaseModel


class Transcript(BaseModel):
    text: str
    start: float
    duration: float


class TranscriptDto(BaseModel):
    text: str
    timestamp: str


class GetTranscriptsResponseDto(BaseModel):
    transcripts: list[TranscriptDto]


class SummarizeTranscriptResponseDto(BaseModel):
    summary: str
