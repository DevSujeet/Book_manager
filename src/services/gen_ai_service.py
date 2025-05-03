import httpx
from src.config.configs import ollama_settings as settings
from src.config.log_config import logger

async def generate_summary_and_genre(content: str) -> dict:
    status = await check_llm()
    logger.info("LLM status:, {status}")
    
    prompt = (
    "You are a helpful assistant that returns valid JSON only.\n\n"
    "TASK:\n"
    "Given the book content below:\n"
    "1. Generate a compelling book marketing summary (~150 words).\n"
    "2. Classify the genre (choose ONE from: horror, romance, action, thriller).\n\n"
    "RULES:\n"
    "- Respond with ONLY a single-line valid JSON object.\n"
    "- No markdown, comments, triple quotes, or extra formatting.\n"
    "- Use this exact format: {\"summary\": \"...\", \"genre\": \"...\"}\n"
    "- Do NOT include explanations or descriptions.\n\n"
    f"Book Content:\n{content}\n"
)


    logger.info("✅ Loaded from .env:, {settings.ollama_url}, {settings.ollama_model}")

    payload = {
        "model": settings.ollama_model,  # Dynamically loaded from .env
        "prompt": prompt,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(f"{settings.ollama_url}/api/generate", json=payload)
        response.raise_for_status()
        return response.json()

async def check_llm():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(f"{settings.ollama_url}")
            return {"status": "ok", "body": r.text}
        except Exception as e:
            return {"status": "fail", "error": str(e)}
