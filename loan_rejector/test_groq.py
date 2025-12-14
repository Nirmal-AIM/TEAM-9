import os
from openai import OpenAI

# Hardcoded clean key to test
api_key = "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"

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
)

try:
    print("Listing models...")
    models = client.models.list()
    # Check if we can find the llama model
    found = False
    for m in models:
        if "llama-3.3-70b" in m.id:
            print(f"Found model: {m.id}")
            found = True
    
    if found:
        print("Success: API key is valid and Llama model found.")
    else:
        print("Success: API key is valid but Llama model not found in list.")
except Exception as e:
    print(f"Error: {e}")
