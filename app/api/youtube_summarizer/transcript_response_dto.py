from pydantic import BaseModel


class Transcript(BaseModel):
    text: str
    start: float
    duration: float


class GetTranscriptsResponseDto(BaseModel):
    transcripts: list[Transcript]


class SummarizeTranscriptResponseDto(BaseModel):
    summary: str
