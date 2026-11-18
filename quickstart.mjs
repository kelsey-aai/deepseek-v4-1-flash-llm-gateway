// Call DeepSeek V4.1 Flash through AssemblyAI LLM Gateway with the OpenAI Node SDK.
// Turn on the DigitalOcean and Fireworks toggles in Data Controls first:
// https://www.assemblyai.com/dashboard/settings/data-controls
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: process.env.LLM_GATEWAY_BASE_URL ?? "https://llm-gateway.assemblyai.com/v1",
  apiKey: process.env.ASSEMBLYAI_API_KEY,
});

const response = await client.chat.completions.create({
  model: "deepseek-v4.1-flash",
  messages: [
    { role: "system", content: "You summarize customer calls in three sentences." },
    {
      role: "user",
      content:
        "Agent: Thanks for calling. Caller: My invoice shows two charges for October. " +
        "Agent: I see the duplicate and I've refunded it; it posts in 3-5 days.",
    },
  ],
  max_tokens: 500,
});

console.log(response.choices[0].message.content);
