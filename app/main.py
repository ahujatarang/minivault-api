"""
main.py - FastAPI application for MiniVault API.

Provides:
- POST /generate: Returns full response to a prompt
- POST /stream-generate: Streams generated response token by token
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

@app.post("/stream-generate")
async def stream_generate(request: PromptInput):
    """
    Accepts a prompt via POST and streams generated response token-by-token using SSE.
    """
    prompt = request.prompt
    full_response = []  # To collect tokens for logging
    
    async def event_generator():
        """
        Inner generator that:
        1. Yields tokens as they're generated
        2. Collects them for final logging
        """
        async for token in stream_response(prompt):
            full_response.append(token)
            yield {"data": token}  # SSE format
            
        # Log the complete response after streaming finishes
        log_interaction(prompt, "".join(full_response))
    
    return EventSourceResponse(event_generator())
