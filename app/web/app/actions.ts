"use server";

import { Browserbase } from "@browserbasehq/sdk";
// import { generateText } from "ai";
// import { google } from "@ai-sdk/google";
import { TranscriptService } from "./api/services/transcript.service";
import { config } from "@/common/config";

export async function startBBSSession() {
  const browserbase = new Browserbase({
    apiKey: config.BROWSERBASE_API_KEY,
  });

  const session = await browserbase.sessions.create({
    projectId: config.BROWSERBASE_PROJECT_ID,
    timeout: 1000,
    proxies: true,
  });

  const debugUrl = await browserbase.sessions.debug(session.id);

  return {
    sessionId: session.id,
    debugUrl: debugUrl.debuggerFullscreenUrl,
  };
}

export async function generateSummary(transcripts: { text: string; timestamp: string }[]) {
  
  const { summary } = await TranscriptService.summarizeTranscript(transcripts);
  return summary;
}