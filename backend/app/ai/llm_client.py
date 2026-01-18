import json
from groq import AsyncGroq
from typing import Dict, Any, Optional
from app.core.config import settings

client = AsyncGroq(api_key=settings.groq_api_key)


async def call_llm(prompt: str, system_prompt: Optional[str] = None, temperature: Optional[float] = None) -> Dict[str, Any]:
    """
    Centralized LLM client for Groq API calls.
    Returns structured JSON output.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        temperature=temperature or settings.groq_temperature,
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("Empty response from Groq API")
    return json.loads(content)

