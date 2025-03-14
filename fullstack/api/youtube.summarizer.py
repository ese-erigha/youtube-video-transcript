import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional
import re


class YouTubeSummarizer:
    def __init__(self):
        """
        Initialize the YouTube Summarizer
        """

        self.llm = ChatOllama(temperature=0, model="llama3.2")

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=1000,
            separators=["\n\n", "\n", " ", ""]
        )

        # Custom prompts for the summary chain
        self.map_prompt_template = """
                Summarize the following part of a YouTube video transcript:
                "{text}"

                KEY POINTS AND TAKEAWAYS:
                """

        self.combine_prompt_template = """
                Create a detailed summary of the YouTube video based on these transcript summaries:
                "{text}"

                Please structure the summary as follows:
                1. Main Topic/Theme
                2. Key Points
                3. Important Details
                4. Conclusions/Takeaways

                DETAILED SUMMARY:
                """

        # Create the summary chain
        self.map_prompt = PromptTemplate(
            template=self.map_prompt_template,
            input_variables=["text"]
        )

        self.combine_prompt = PromptTemplate(
            template=self.combine_prompt_template,
            input_variables=["text"]
        )

        self.chain = load_summarize_chain(
            llm=self.llm,
            chain_type="map_reduce",
            map_prompt=self.map_prompt,
            combine_prompt=self.combine_prompt,
            verbose=False
        )

    def extract_video_id(self, youtube_url: str) -> Optional[str]:
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

    def get_transcripts(self, video_id: str) -> list[dict[str, str]]:
        """
            Get the list of transcript of a YouTube video

            Args:
                video_id (str): YouTube video ID

            Returns:
                list[dict[str, str]]: list of transcript object
        """
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript_list
        except Exception as e:
            raise Exception(f"Error getting transcripts: {str(e)}")

    def get_transcript(self, video_id: str) -> str:
        """
        Get the transcript of a YouTube video

        Args:
            video_id (str): YouTube video ID

        Returns:
            str: Combined transcript text
        """
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            for entry in transcript_list:
                print(entry)

            return " ".join([entry['text'] for entry in transcript_list])
        except Exception as e:
            raise Exception(f"Error getting transcript: {str(e)}")

    def summarize_transcripts(self, transcript_list: list[dict[str, str]]) -> str:
        """
            Summarize a list of transcript

                Args:
                    transcript_list list[dict[str, str]]: List of transcript

                Returns:
                    dict: Summary result with status and content
        """
        transcript = " ".join([entry['text'] for entry in transcript_list])

        # Split transcript into chunks
        documents = self.text_splitter.create_documents([transcript])

        # Generate summary
        summary = self.chain.invoke({"input_documents": documents})

        return summary["output_text"]

    def summarize_video(self, youtube_url: str) -> dict:
        """
        Summarize a YouTube video given its URL

        Args:
            youtube_url (str): YouTube video URL

        Returns:
            dict: Summary result with status and content
        """
        try:
            # Extract video ID
            video_id = self.extract_video_id(youtube_url)
            if not video_id:
                return {
                    "status": "error",
                    "message": "Invalid YouTube URL"
                }

            # Get transcript
            transcript = self.get_transcript(video_id)

            # Split transcript into chunks
            documents = self.text_splitter.create_documents([transcript])

            # Generate summary
            summary = self.chain.invoke({"input_documents": documents})

            return {
                "status": "success",
                "summary": summary,
                "video_id": video_id
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


def main():
    # Initialize summarizer
    summarizer = YouTubeSummarizer()

    # Example YouTube video URL
    video_url = "https://youtu.be/6K3wiD6ACWg?si=WYbngXId1RW28ADr"

    # Get summary
    result = summarizer.summarize_video(video_url)

    if result["status"] == "success":
        # for key, value in result["summary"].items():
        #     print(key)
        print("\nVideo Summary:")
        # print(result["summary"]["output_text"])
    else:
        print(f"\nError: {result['message']}")


if __name__ == "__main__":
    main()
