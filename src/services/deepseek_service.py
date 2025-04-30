import httpx
from src.config.configs import ollama_settings as settings

async def generate_summary_and_genre(content: str) -> dict:
    prompt = (
        "You are a book marketing expert.\n"
        "Given the content below, please:\n"
        "1. Write an attractive marketing-style book summary (~150 words).\n"
        "2. Predict the genre (choose exactly one: horror, romance, action, thriller).\n"
        "Respond ONLY in JSON format: {\"summary\": \"...\", \"genre\": \"romance\"}.\n\n"
        f"Book Content:\n{content}"
    )

    payload = {
        "model": "deepseek-coder:1.3b", # "model": "deepseek:1.3b",
        "prompt": prompt,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(f"{settings.ollama_url}/api/generate", json=payload)
        response.raise_for_status()
        return response.json()
