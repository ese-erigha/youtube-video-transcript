from fastapi import HTTPException
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional
import re
from .transcript_response_dto import Transcript


class GetTranscriptsUsecase:
    @staticmethod
    def extract_video_id(youtube_url: str) -> Optional[str]:
        """
        Extract video ID from various forms of YouTube URLs

        Args:
            youtube_url (str): YouTube video URL

        Returns:
            str: Video ID if found, None otherwise
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?]*)',
            r'(?:youtube\.com\/shorts\/)([^&\n?]*)'
        ]

        for pattern in patterns:
            match = re.search(pattern, youtube_url)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def execute(video_url) -> list[Transcript]:
        """
            Get the list of transcript of a YouTube video

            Args:
                video_url (str): YouTube video URL

            Returns:
                list[dict[str, str]]: list of transcript object
        """
        video_id = GetTranscriptsUsecase.extract_video_id(video_url)
        if video_id is None:
            raise HTTPException(status_code=400, detail="Invalid video url")

        try:

            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript_list
        except Exception as e:
            raise Exception(f"Error getting transcripts: {str(e)}")
