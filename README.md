# MiniVault API

A lightweight local REST API that simulates a core feature of ModelVault: receiving a prompt and returning a generated response using a local LLM.

## Features

- POST `/generate` — Generate a full response
- GET `/stream-generate` — Stream token-by-token response
- All interactions are logged in `logs/log.jsonl`
- CLI tool included for easy testing

## Setup Instructions

1. **Clone the repo** and navigate into the folder:
   ```bash
   git clone https://github.com/your-username/minivault-api.git
   cd minivault-api

8. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

7. Install dependencies:
   ```bash
   pip install -r requirements.txt

6. Run the API:
   ```bash
   uvicorn app.main:app --reload

5. Use CLI:
   ```bash
   python app/cli.py

## Notes

Uses distilgpt2 model from HuggingFace.
All runs are offline — no external APIs used.
Designed to be fast, readable, and minimal.

## Future Improvements

Add more models using Ollama or ggml.
Improve logging with rotation.
Add unit tests for API routes and CLI.

