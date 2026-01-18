import json
from groq import AsyncGroq
from typing import Dict, Any, Optional
from app.core.config import settings

# Initialize client only if API key is available
client = AsyncGroq(api_key=settings.groq_api_key) if settings.groq_api_key else None


async def call_llm(prompt: str, system_prompt: Optional[str] = None, temperature: Optional[float] = None) -> Dict[str, Any]:
    """
    Centralized LLM client for Groq API calls.
    Returns structured JSON output.
    """
    if not client or not settings.groq_api_key:
        raise ValueError(
            "AI service not available. GROQ_API_KEY environment variable is not set. "
            "Get a free API key at https://console.groq.com"
        )
    
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

