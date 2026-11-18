"""Transcribe a long recording with AssemblyAI-STT-3.7, then summarize it with
DeepSeek V4.1 Flash on LLM Gateway, using one API key.

The Gateway fetches the transcript text itself when you pass `transcript_id`
and put the literal tag {{ transcript }} in your message. A fallback model
handles a failed DeepSeek request.

Usage: python summarize_recording.py path/or/url/to/meeting.mp3
"""
import os
import sys

import assemblyai as aai
from openai import OpenAI

API_KEY = os.environ["ASSEMBLYAI_API_KEY"]
GATEWAY_URL = os.environ.get("LLM_GATEWAY_BASE_URL", "https://llm-gateway.assemblyai.com/v1")

PRIMARY_MODEL = "deepseek-v4.1-flash"
FALLBACK_MODEL = "claude-opus-5-5"  # next-highest 1-hour summarization score on Voice Standard Bench

SUMMARY_PROMPT = (
    "Summarize this meeting for someone who missed it. List the decisions, the action "
    "items with their owners, and any open questions. Use only what the transcript says.\n\n"
    "Transcript:\n{{ transcript }}"
)


def transcribe(audio: str) -> str:
    """Return the ID of a completed transcript."""
    aai.settings.api_key = API_KEY
    config = aai.TranscriptionConfig(speech_models=["assemblyai-stt-3-7"], speaker_labels=True)
    transcript = aai.Transcriber().transcribe(audio, config=config)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")
    return transcript.id


def summarize(transcript_id: str) -> str:
    client = OpenAI(base_url=GATEWAY_URL, api_key=API_KEY, timeout=600)
    response = client.chat.completions.create(
        model=PRIMARY_MODEL,
        messages=[{"role": "user", "content": SUMMARY_PROMPT}],
        max_tokens=2000,
        # LLM Gateway fields that the OpenAI SDK doesn't know about go in extra_body
        extra_body={
            "transcript_id": transcript_id,
            "fallbacks": [{"model": FALLBACK_MODEL}],
        },
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python summarize_recording.py <audio file or URL>")
    tid = transcribe(sys.argv[1])
    print(summarize(tid))
