import pytest
from fastapi.testclient import TestClient
from src.tik_tok.main import app

@pytest.mark.asyncio
async def test_health_check():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

