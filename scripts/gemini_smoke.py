#!/usr/bin/env python3
"""
scripts/gemini_smoke.py
Smoke test for Gemini API connectivity.
Reads configuration from backend/.env.
Never logs or prints the API key or raw exception messages.
Prints only: 'OK model=<name> latencyMs=<n>' or 'ERROR error_class=<ExceptionClass>'
"""
import os
import sys
import time
from pathlib import Path

# Locate backend/.env
repo_root = Path(__file__).resolve().parent.parent
env_path = repo_root / "backend" / ".env"

try:
    import dotenv
    dotenv.load_dotenv(env_path)
except ImportError:
    pass

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"

if not api_key:
    print("ERROR error_class=MissingApiKeyError: GEMINI_API_KEY not set in backend/.env")
    sys.exit(1)

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR error_class=ImportError: google-genai is not installed")
    sys.exit(1)

start_time = time.perf_counter()

try:
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=8.0)
    )
    response = client.models.generate_content(
        model=model_name,
        contents="Say OK in one word."
    )
    latency_ms = int((time.perf_counter() - start_time) * 1000)
    print(f"OK model={model_name} latencyMs={latency_ms}")
    sys.exit(0)
except Exception as e:
    err_class = type(e).__name__
    print(f"ERROR error_class={err_class}")
    sys.exit(1)
