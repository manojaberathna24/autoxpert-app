import os
import json
from typing import Any, Dict, Optional

import requests


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


def _get_api_key() -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    # Streamlit secrets support (optional, avoids importing streamlit here)
    if not api_key:
        try:
            import streamlit as st  # type: ignore

            if "OPENROUTER_API_KEY" in st.secrets:
                api_key = st.secrets["OPENROUTER_API_KEY"]
        except Exception:
            pass
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Configure it as an environment variable or in Streamlit secrets."
        )
    return api_key


def call_openrouter_json(
    system_prompt: str,
    user_payload: Dict[str, Any],
    model: str = "openai/gpt-4.1-mini",
    temperature: float = 0.3,
) -> Dict[str, Any]:
    """
    Call OpenRouter with a structured JSON-style prompt and parse the response as JSON.
    """
    api_key = _get_api_key()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": "Here is the data in JSON format. Respond ONLY with valid JSON as specified previously.\n"
            + json.dumps(user_payload, ensure_ascii=False),
        },
    ]

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
    }

    resp = requests.post(OPENROUTER_BASE_URL, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"OpenRouter error {resp.status_code}: {resp.text}")

    data = resp.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected OpenRouter response format: {data}") from e

    # Ensure we have a JSON object
    if isinstance(content, dict):
        return content
    if isinstance(content, str):
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON from model response: {content}") from e

    raise RuntimeError(f"Unsupported content type from OpenRouter: {type(content)}")


