import os
from pathlib import Path


def load_prompt(prompt_name: str) -> str:
    """Load prompt template from ai/prompts/ directory."""
    prompt_dir = Path(__file__).parent.parent / "ai" / "prompts"
    prompt_path = prompt_dir / f"{prompt_name}.txt"
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

