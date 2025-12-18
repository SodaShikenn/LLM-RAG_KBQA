from helper import *

print("Testing embedding function...")
try:
    resp = get_llm_embedding('test text')
    print(f"✓ Embedding function works! Embedding dimension: {len(resp.data[0].embedding)}")
except Exception as e:
    print(f"✗ Embedding function failed: {e}")

print("\nTesting chat completion function...")
try:
    resp = get_llm_chat([
        {'role': 'user', 'content': 'Say hello'}
    ], 'qwen-max')
    print(f"✓ Chat function works! Response: {resp.choices[0].message.content}")
except Exception as e:
    print(f"✗ Chat function failed: {e}")

print("\nTesting segment_text function...")
text = "a" * 1000
segments = segment_text(text, segment_length=500, overlap=100)
print(f"✓ Segment function works! Created {len(segments)} segments")

print("\nTesting allowed_file function...")
print(f"test.txt allowed: {allowed_file('test.txt')}")
print(f"test.exe allowed: {allowed_file('test.exe')}")
