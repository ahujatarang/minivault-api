"""
CLI tool to interact with the MiniVault API.
Supports both standard and streaming prompt generation modes.
"""

import requests

def call_generate():
    """Sends a POST request to /generate and prints the full response."""
    prompt = input("Enter a prompt: ")
    res = requests.post("http://127.0.0.1:8000/generate", json={"prompt": prompt})
    print("\nResponse:")
    print(res.json()["response"])

def call_stream():
    """Sends a GET request to /stream-generate and prints tokens as they stream in."""
    prompt = input("Enter a prompt: ")
    print("\nStreaming response:\n")

    with requests.get(
        "http://127.0.0.1:8000/stream-generate",
        params={"prompt": prompt},
        stream=True,
    ) as res:
        for line in res.iter_lines(decode_unicode=True):
            line = line.strip()
            if line.startswith("data:"):
                token = line[len("data:"):].strip()
                if token:
                    print(token, flush=True)

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Standard generate")
    print("2. Stream generate")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        call_generate()
    elif choice == "2":
        call_stream()
    else:
        print("Invalid choice.")
