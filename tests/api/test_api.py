from fastapi.testclient import TestClient
from app.web import app

client = TestClient(app)


def test_study_endpoint():

    response = client.post(
        "/study",
        json={"topic": "Python"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data
    assert "questions" in data
    assert "answers" in data