import pytest
import httpx
from src.services.gen_ai_service import generate_summary_and_genre

@pytest.mark.asyncio
async def test_generate_summary_and_genre(monkeypatch):
    # Mock response JSON
    pass
