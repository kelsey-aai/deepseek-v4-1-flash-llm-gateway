"""Call DeepSeek V4.1 Flash through AssemblyAI LLM Gateway with the OpenAI Python SDK.

Before you run this, turn on the opt-in providers that serve DeepSeek V4.1 Flash
(DigitalOcean and Fireworks) on the Data Controls page of your AssemblyAI dashboard:
https://www.assemblyai.com/dashboard/settings/data-controls
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("LLM_GATEWAY_BASE_URL", "https://llm-gateway.assemblyai.com/v1"),
    api_key=os.environ["ASSEMBLYAI_API_KEY"],
)

response = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[
        {"role": "system", "content": "You summarize customer calls in three sentences."},
        {
            "role": "user",
            "content": "Agent: Thanks for calling. Caller: My invoice shows two charges "
            "for October. Agent: I see the duplicate and I've refunded it; it posts in 3-5 days.",
        },
    ],
    max_tokens=500,
)

print(response.choices[0].message.content)
