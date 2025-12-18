from helper import *

print("Testing chat completion with gpt-4o-mini...")
try:
    resp = get_llm_chat([
        {'role': 'user', 'content': 'Say hello'}
    ], 'gpt-4o-mini')
    print(f"✓ GPT-4o-mini works! Response: {resp.choices[0].message.content}")
except Exception as e:
    print(f"✗ GPT-4o-mini failed: {e}")
