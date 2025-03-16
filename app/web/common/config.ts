import { z } from "zod";

const configSchema = z.object({
    API_BASE_URL: z.string().nonempty(),
    GET_TRANSCRIPTS_PATH_URL: z.string().nonempty(),
    SUMMARIZE_TRANSCRIPTS_PATH_URL: z.string().nonempty(),
    BROWSERBASE_API_KEY: z.string().nonempty(),
    BROWSERBASE_PROJECT_ID: z.string().nonempty(),
    OPENAI_API_KEY: z.string().nonempty(),
});

type Config = Required<z.infer<typeof configSchema>>;

export const config: Config = configSchema.parse(process.env); 