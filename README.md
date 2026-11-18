# DeepSeek V4.1 Flash API through AssemblyAI LLM Gateway

Call DeepSeek V4.1 Flash (`deepseek-v4.1-flash`) with the OpenAI SDK through [AssemblyAI LLM Gateway](https://www.assemblyai.com/products/llm-gateway), and run it on your own recordings with the same API key you use for Speech-to-Text.

Companion code for the AssemblyAI blog post "How to use the DeepSeek V4.1 Flash API (pricing, context window, quickstart)".

## What's here

| File | What it does |
| --- | --- |
| `quickstart.py` | OpenAI Python SDK call to `deepseek-v4.1-flash` |
| `quickstart.mjs` | OpenAI Node SDK call |
| `quickstart.sh` | The same request with curl |
| `summarize_recording.py` | Transcribes a file with AssemblyAI-STT-3.7, then summarizes it with DeepSeek V4.1 Flash using `transcript_id` injection and a fallback model |
| `bench_lookup.py` | Prints the model's specs and Voice Standard Bench results from the public models endpoint (no key needed) |

## Before you start: turn on the opt-in providers

DeepSeek V4.1 Flash is served by DigitalOcean (the default provider) and Fireworks. Both are opt-in providers on LLM Gateway, so they're off by default. Turn on their toggles on the [Data Controls](https://www.assemblyai.com/dashboard/settings/data-controls) page in your dashboard before you send a request. See [Providers](https://www.assemblyai.com/docs/llm-gateway/providers) for each provider's retention and BAA status.

## Setup

```bash
cp .env.example .env          # add your AssemblyAI API key
export $(cat .env | xargs)

# Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python quickstart.py
python summarize_recording.py https://assembly.ai/wildfires.mp3
python bench_lookup.py                       # or: python bench_lookup.py deepseek-v4.1-flash-1017

# Node.js (18+)
npm install
node quickstart.mjs

# curl
./quickstart.sh
```

## Notes

- Base URL: `https://llm-gateway.assemblyai.com/v1`. DeepSeek V4.1 Flash is listed for the US region only, so don't point it at the EU endpoint.
- `transcript_id` and `fallbacks` are LLM Gateway fields, so the OpenAI SDK sends them through `extra_body`.
- Hour-long transcripts can take a minute or more to summarize on this model, so the Python client sets a 600-second timeout.
- Prices, regions and benchmark results change. `bench_lookup.py` reads them live from `https://llm-gateway.assemblyai.com/v1/models`.

## License

MIT
