export interface Transcript {
  text: string;
  timestamp: string;
}

export interface GetTranscriptsResponseDto{
  transcripts: Transcript[];
}

export interface GetTranscriptSummaryResponseDto{
  summary: string;
}