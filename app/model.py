"""
model.py – Handles local text generation using DistilGPT2.
Includes:
- Full response generation (generate_response)
- Token-by-token streaming (stream_response)
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import asyncio

# Load tokenizer and model once (at import time)
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")
model.eval()  # Set to evaluation mode (no gradients needed)


def generate_response(prompt: str) -> str:
    """
    Generate a complete response for the given prompt using DistilGPT2.
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,                       # Unpacks input_ids
        max_new_tokens=100,             # Generate up to 100 new tokens
        do_sample=True,                 # Enable sampling (for randomness)
        top_k=50,                       # Limits sampling pool to top 50 tokens
        top_p=0.95,                     # Nucleus (top-p) sampling
        repetition_penalty=1.1,         # Reduces word repetition
        pad_token_id=tokenizer.eos_token_id  # Avoid warning about padding
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


async def stream_response(prompt: str):
    """
    Asynchronously stream response token-by-token for the given prompt.
    Yields one token at a time.
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"]
    output_ids = input_ids.clone()  # Start with the prompt

    for _ in range(100):  # Limit to 100 generated tokens
        outputs = model(output_ids)
        next_token_logits = outputs.logits[:, -1, :]
        next_token_id = torch.argmax(next_token_logits, dim=-1).unsqueeze(0)
        output_ids = torch.cat([output_ids, next_token_id], dim=-1)
            
        # Decode only the newly generated token
        token_text = tokenizer.decode(next_token_id[0], skip_special_tokens=True)
        
        if token_text: 
            yield token_text

