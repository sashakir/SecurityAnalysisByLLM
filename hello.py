import openai
client = openai.OpenAI(
    api_key="",
    base_url="https://litellm.labs.jb.gg/" # LiteLLM Proxy is OpenAI compatible, Read More: https://docs.litellm.ai/docs/proxy/user_keys
)

response = client.chat.completions.create(
    model="gpt-4o-mini", # model to send to the proxy (more capable default)
    messages = [
        {
            "role": "user",
            "content": "this is a test request, write a short poem in russian like Pushkin"
        }
    ]
)

try:
    # OpenAI-style SDKs typically expose: choices[0].message.content
    print("Assistant:", response.choices[0].message.content)
except Exception:
    # Fallback in case the SDK returns dict-like objects
    try:
        print("Assistant:", response.choices[0].message["content"]) 
    except Exception:
        print("Assistant: <unable to parse content>")

