#!/usr/bin/env bash
# Call DeepSeek V4.1 Flash through AssemblyAI LLM Gateway with curl.
# Turn on the DigitalOcean and Fireworks toggles in Data Controls first.
set -euo pipefail
BASE_URL="${LLM_GATEWAY_BASE_URL:-https://llm-gateway.assemblyai.com/v1}"

curl -sS "$BASE_URL/chat/completions" \
  -H "Authorization: $ASSEMBLYAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4.1-flash",
    "messages": [
      {"role": "system", "content": "You summarize customer calls in three sentences."},
      {"role": "user", "content": "Agent: Thanks for calling. Caller: My invoice shows two charges for October. Agent: I see the duplicate and I have refunded it; it posts in 3-5 days."}
    ],
    "max_tokens": 500
  }'
echo
