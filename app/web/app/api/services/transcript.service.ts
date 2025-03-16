import { GetTranscriptsResponseDto, Transcript, GetTranscriptSummaryResponseDto } from "@/common/types";
import { HTTPClientService } from "../http.client";
import { config } from "@/common/config";

export class TranscriptService{
    public static async getTranscripts(video_url: string): Promise<GetTranscriptsResponseDto>{
        const path_url = config.GET_TRANSCRIPTS_PATH_URL;
        const params = {video_url };
        const response = await HTTPClientService.fetchData<GetTranscriptsResponseDto>(path_url, { params });
        return response;
    }

    public static async summarizeTranscript(transcripts: Transcript[]): Promise<GetTranscriptSummaryResponseDto>{
        const transcript = transcripts.map((transcript)=> transcript.text).join(" ");
        const path_url = config.SUMMARIZE_TRANSCRIPTS_PATH_URL;
        const params = { transcript };
        const response = await HTTPClientService.fetchData<GetTranscriptSummaryResponseDto>(path_url, { params });
        return response;
    }
    
}