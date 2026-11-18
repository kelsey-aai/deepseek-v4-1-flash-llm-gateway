"""Print DeepSeek V4.1 Flash's Voice Standard Bench results from the public
LLM Gateway models endpoint. No API key needed.

Usage: python bench_lookup.py [model_id]
"""
import os
import sys

import requests

MODELS_URL = os.environ.get("LLM_GATEWAY_BASE_URL", "https://llm-gateway.assemblyai.com/v1") + "/models"
model_id = sys.argv[1] if len(sys.argv) > 1 else "deepseek-v4.1-flash"

models = requests.get(MODELS_URL, timeout=30).json()["data"]
model = next((m for m in models if m["id"] == model_id), None)
if model is None:
    sys.exit(f"{model_id} is not in the catalog")

price = model["pricing"]["global"]
print(f"{model['name']} ({model['id']})")
print(f"  context: {model['context_length']:,} tokens, regions: {', '.join(model['available_regions'])}")
print(f"  providers: {', '.join(p['name'] for p in model['providers'])} (default: {model['default_provider']['name']})")
print(f"  price per 1M tokens: ${price['prompt']} in / ${price['completions']} out")
print()
print(f"{'bucket':>7} {'overall':>7} {'summ':>5} {'extract':>7} {'correct':>7} {'dict':>5} {'$/audio hr':>10} {'p50 s':>7} {'p95 s':>7}")
for row in (model.get("performance") or {}).get("data", []):
    tq = row["task_quality"]
    print(
        f"{row['bucket']:>7} {row['quality_score']:>7} {tq['summarization']:>5} "
        f"{tq['information_extraction']:>7} {tq['text_correction']:>7} {tq['dictation'] or '-':>5} "
        f"{row['cost_per_hour_usd']:>10.4f} {row['latency']['p50']:>7.1f} {row['latency']['p95']:>7.1f}"
    )
