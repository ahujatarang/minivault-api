"""
main.py - FastAPI application for MiniVault API.

Provides:
- POST /generate: Returns full response to a prompt
- GET /stream-generate: Streams generated response token by token
"""

from fastapi import FastAPI
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from model import generate_response, stream_response
from logger import log_interaction

app = FastAPI()

class PromptInput(BaseModel):
    prompt: str

@app.post("/generate")
def generate(request: PromptInput):
    """
    Accepts a prompt via POST and returns a full generated response.
    """
    prompt = request.prompt
    response = generate_response(prompt)
    log_interaction(prompt, response)
    return {"response": response}

@app.get("/stream-generate")
async def stream_generate(prompt: str):
    """
    Accepts a prompt via GET and streams generated response token-by-token using SSE.
    """
    async def event_generator():
        async for token in stream_response(prompt):
            yield f"data: {token}\n\n"  # SSE requires this format

    return EventSourceResponse(event_generator())
