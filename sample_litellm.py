"""
Sample program using the LiteLLM API.

Prerequisites:
- Python 3.9+
- Install dependency: pip install litellm
- Set provider API key in your environment (examples):
  * OpenAI: export OPENAI_API_KEY="sk-..."
  * Anthropic: export ANTHROPIC_API_KEY="..."
  * Google Vertex AI (via LiteLLM): configure GOOGLE_APPLICATION_CREDENTIALS, etc.

Usage:
  python sample_litellm.py "Write a haiku about the sea"

You can also set the model via env var MODEL (defaults to gpt-4o-mini or any model you prefer):
  export MODEL="gpt-4o-mini"

LiteLLM routes to many providers with a unified interface.
See: https://docs.litellm.ai/ for supported models and provider keys.
"""
from __future__ import annotations

import os
import sys
from typing import List, Dict, Any

try:
    # Core LiteLLM chat completion API
    from litellm import completion
except Exception as e:  # pragma: no cover
    print("LiteLLM is not installed. Run: pip install litellm", file=sys.stderr)
    raise

def get_prompt_from_argv() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()
    return "Say hello and introduce yourself in one sentence."


def build_messages(user_prompt: str) -> List[Dict[str, Any]]:
    """Return a minimal chat message list for LiteLLM.

    Why two messages (system and user) and what's the difference?
    - system: High-level behavior and rules for the assistant. It sets the "persona"
      and guardrails. The model uses this as overarching guidance that applies to
      the entire conversation.
    - user: The actual request or task to perform. This is the user's prompt or
      question. The assistant should follow the system instructions while answering
      the user.
    """
    # System message defines assistant behavior and constraints
    system_msg = {
        "role": "system",
        "content": "You are a helpful assistant. Keep responses concise unless asked for detail.",
    }
    # User message contains the concrete instruction/request
    user_msg = {"role": "user", "content": user_prompt}
    return [system_msg, user_msg]


def print_response(resp: Any) -> None:
    """Print the assistant message from a LiteLLM response object."""
    try:
        # OpenAI-style: resp.choices[0].message["content"]
        content = resp.choices[0].message["content"]
    except Exception:
        content = str(resp)
    print("\nAssistant:\n" + content)


def run_non_streaming(model: str, messages: List[Dict[str, Any]]) -> None:
    print(f"Running non-streaming completion with model={model}...")
    resp = completion(model=model, messages=messages)
    print_response(resp)


def run_streaming(model: str, messages: List[Dict[str, Any]]) -> None:
    print(f"\nRunning streaming completion with model={model}...")
    # LiteLLM streaming returns a generator of chunks similar to OpenAI SSE chunks
    stream = completion(model=model, messages=messages, stream=True)
    print("\nAssistant (streamed):\n", end="", flush=True)
    for chunk in stream:
        try:
            delta = chunk.choices[0].delta.get("content", "")
        except Exception:
            delta = ""
        if delta:
            print(delta, end="", flush=True)
    print()  # newline after stream completes


def main() -> None:
    # Choose a default model that is widely available via LiteLLM routing.
    # You can set MODEL env var to override, e.g., gpt-4o-mini, gpt-3.5-turbo, claude-3-5-sonnet-latest, gemini/gemini-1.5-pro, etc.
    model = os.getenv("MODEL", "gpt-4o-mini")

    # Ensure at least one provider API key is set. LiteLLM looks for provider-specific env vars.
    # We don't hard-require a particular provider here, but we can warn if likely missing.
    has_any_key = any(
        os.getenv(k)
        for k in (
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GROQ_API_KEY",
            "COHERE_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "TOGETHERAI_API_KEY",
            "MISTRAL_API_KEY",
            "DEEPSEEK_API_KEY",
            "XAI_API_KEY",
            "PERPLEXITY_API_KEY",
        )
    )
    if not has_any_key:
        print(
            "Warning: No provider API key detected. Set an appropriate env var, e.g., OPENAI_API_KEY.",
            file=sys.stderr,
        )

    prompt = get_prompt_from_argv()
    messages = build_messages(prompt)

    # Run a simple non-streaming completion
    run_non_streaming(model, messages)

    # And an optional streaming example (some providers/models may not support streaming)
    try:
        run_streaming(model, messages)
    except Exception as e:  # pragma: no cover
        print(f"Streaming failed or unsupported for model '{model}': {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
