import pytest
from app.app import app

@pytest.fixture
def client():
	return app.test_client()



def test_health(client):
	response= client.get("/health")
	assert response.status_code == 200
def test_analyze_positive(client):
	response=client.post("/analyze", 
			json={"text": "i love this product"})
	assert response.get_json()["sentiment"] == "positive"
