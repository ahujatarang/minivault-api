"""
CLI tool to interact with the MiniVault API.
Supports both standard and streaming prompt generation modes.
"""

import requests
import sys

def call_generate():
    """Sends a POST request to /generate and prints the full response."""
    try:
        prompt = input("Enter a prompt: ")
        if not prompt.strip():
            print("Error: Prompt cannot be empty")
            return
                
        res = requests.post("http://127.0.0.1:8000/generate", json={"prompt": prompt}, timeout=30)
        res.raise_for_status()
    
        print("\nResponse:")
        print(res.json()["response"])
    
    except requests.exceptions.RequestException as e:
        print(f"\nError: Failed to get response - {str(e)}", file=sys.stderr)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}", file=sys.stderr)

def call_stream():
    """Sends a POST request to /stream-generate and prints tokens as they stream in."""
    try:
        prompt = input("Enter a prompt: ")
        if not prompt.strip():
            print("Error: Prompt cannot be empty")
            return
        print("\nStreaming response:\n")

        with requests.post(
            "http://127.0.0.1:8000/stream-generate",
            json={"prompt": prompt},
            stream=True,
        ) as res:
            res.raise_for_status()
            for line in res.iter_lines(decode_unicode=True):
                if line:
                    line = line.strip()
                    if line.startswith("data:"):
                        token = line[len("data:"):].strip()
                        if token:
                            print(token, flush=True, end=" ")
                    
    except requests.exceptions.RequestException as e:
        print(f"\nError: Failed to stream response - {str(e)}", file=sys.stderr)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}", file=sys.stderr)    

if __name__ == "__main__":
    try:
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
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
