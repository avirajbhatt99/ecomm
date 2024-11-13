from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)


def test_health_check():
    """
    test case for health check
    """
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is healthy"}
