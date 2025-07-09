# MiniVault API

A lightweight local REST API that simulates ModelVault's core feature: receiving prompts and returning generated responses using a local LLM.

---

## 🚀 Features

- POST `/generate` — Generate a full response
- POST `/stream-generate` — Stream token-by-token response
- All interactions are logged in `logs/log.jsonl`
- CLI tool for easy testing

---

## 🧠 Technologies Used

- Python 3.9
- FastAPI: REST API framework
- Uvicorn: ASGI server
- Hugging Face Transformers: DistilGPT2 model
- PyTorch: Model backend
- sse-starlette: Server-Sent Events
- Requests: CLI HTTP client

---

## 📁 Project Structure

```
minivault-api/
├── app/
│   ├── main.py            # FastAPI endpoints (generate + stream)
│   ├── model.py           # LLM interactions
│   ├── logger.py          # Logging utility
│   └── cli.py             # Command-line interface
├── logs/
│   └── gitkeep            # Placeholder (log.jsonl auto-created at runtime)
├── requirements.txt       # Dependencies
└── README.md
```

**Note**: The `logs/log.jsonl` file will be automatically generated when you first run the API, containing all prompt/response pairs in JSONL format.
Sample entry format:
```json
{"timestamp": "2025-07-09T11:13:25.169206", "prompt": "Hello", "response": "Hello! Welcome to ModelVault's API simulation. How can I assist you today?"}
```   
---

## 🏁 Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/minivault-api.git
   cd minivault-api

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Run API server**:
   ```bash
   uvicorn app.main:app --reload

5. **Use CLI**(in second terminal):
   ```bash
   python app/cli.py

6. **Alternative testing with curl**:
   ```bash
   # Complete response
   curl -X POST http://localhost:8000/generate \
      -H "Content-Type: application/json" \
      -d '{"prompt":"Hello"}'
   
   # Stream response
   curl -X POST http://localhost:8000/stream-generate \
      -H "Content-Type: application/json" \
      -d '{"prompt":"Hello"}' \
      --no-buffer
   
---

## 🔧 Tradeoffs & Design Choices

- Model Selection:
     - Used DistilGPT2 (smaller/faster) instead of larger models
     - Tradeoff: Less creative output vs. full GPT-2
- Streaming Implementation:
     - POST method for RESTful compliance
     - Tradeoff: More complex than GET but more secure
- Logging:
     - Simple JSONL format for readability
     - Tradeoff: No rotation/compression (prioritized MVP)
- Performance:
     - Model loaded once at startup
     - Tradeoff: Higher memory usage vs. on-demand loading

---

## 📌 Notes

- Uses DistilGPT2 model from HuggingFace.
- All runs are offline — no cloud APIs used.
- Designed to be fast, readable, and minimal.

---

## 🧪 Future Improvements

- Add more models using Ollama or ggml.
- Improve logging with rotation/compression.
- Add unit tests for API routes and CLI.

