import pytest
from fastapi.testclient import TestClient
from app.web import app
from app.storage.mongodb_store import clear_all

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_db():
    """Clear database before and after each test."""
    clear_all()
    yield
    clear_all()


class TestStudyEndpoint:
    """Test the /study endpoint."""

    def test_study_valid_topic(self):
        """Test study endpoint with valid topic."""
        response = client.post("/study", json={"topic": "Python Basics"})
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "key_points" in data
        assert "questions" in data
        assert "answers" in data
        assert isinstance(data["key_points"], list)
        assert isinstance(data["questions"], list)
        assert isinstance(data["answers"], list)

    def test_study_empty_topic(self):
        """Test study endpoint with empty topic."""
        response = client.post("/study", json={"topic": ""})
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]

    def test_study_aws_topic(self):
        """Test study endpoint with AWS S3 topic."""
        response = client.post("/study", json={"topic": "AWS S3"})
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert len(data["answers"]) > 0


class TestInteractionsListEndpoint:
    """Test the GET /interactions endpoint."""

    def test_list_empty(self):
        """Test listing interactions when none exist."""
        response = client.get("/interactions")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_list_after_study(self):
        """Test listing interactions after saving one."""
        client.post("/study", json={"topic": "Python"})
        response = client.get("/interactions")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["topic"] == "Python"
        assert "id" in data[0]
        assert "created_at" in data[0]

    def test_list_multiple(self):
        """Test listing multiple interactions."""
        topics = ["Python", "JavaScript", "Go"]
        for topic in topics:
            client.post("/study", json={"topic": topic})
        
        response = client.get("/interactions")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        returned_topics = {item["topic"] for item in data}
        assert returned_topics == {"Python", "JavaScript", "Go"}

    def test_list_with_limit(self):
        """Test listing with limit parameter."""
        for i in range(5):
            client.post("/study", json={"topic": f"Topic {i}"})
        
        response = client.get("/interactions?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


class TestGetStudyEndpoint:
    """Test the GET /interactions/{topic} endpoint."""

    def test_get_existing_study(self):
        """Test retrieving an existing study material."""
        client.post("/study", json={"topic": "Python"})
        response = client.get("/interactions/Python")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "key_points" in data
        assert "questions" in data
        assert "answers" in data

    def test_get_nonexistent_study(self):
        """Test retrieving a non-existent study."""
        response = client.get("/interactions/NonExistent")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_get_with_special_characters(self):
        """Test retrieving study with special characters in topic."""
        topic = "What is AWS S3?"
        client.post("/study", json={"topic": topic})
        response = client.get(f"/interactions/{topic}")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data


class TestSearchEndpoint:
    """Test the GET /interactions/search endpoint."""

    def test_search_exact_match(self):
        """Test search with exact match."""
        client.post("/study", json={"topic": "Python Programming"})
        response = client.get("/interactions/search?q=Python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["topic"] == "Python Programming"

    def test_search_partial_match(self):
        """Test search with partial match."""
        client.post("/study", json={"topic": "Python Programming"})
        response = client.get("/interactions/search?q=Pro")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "Programming" in data[0]["topic"]

    def test_search_case_insensitive(self):
        """Test search is case-insensitive."""
        client.post("/study", json={"topic": "AWS S3"})
        
        for query in ["aws", "AWS", "Aws", "aWs"]:
            response = client.get(f"/interactions/search?q={query}")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["topic"] == "AWS S3"

    def test_search_multiple_results(self):
        """Test search returning multiple results."""
        topics = ["Python Basics", "Python Advanced", "JavaScript"]
        for topic in topics:
            client.post("/study", json={"topic": topic})
        
        response = client.get("/interactions/search?q=Python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        topics_returned = {item["topic"] for item in data}
        assert "Python Basics" in topics_returned
        assert "Python Advanced" in topics_returned

    def test_search_no_results(self):
        """Test search with no matching results."""
        client.post("/study", json={"topic": "Python"})
        response = client.get("/interactions/search?q=NonExistentQuery")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_search_with_special_characters(self):
        """Test search handles special characters."""
        client.post("/study", json={"topic": "What is AWS S3?"})
        response = client.get("/interactions/search?q=What")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_search_with_limit(self):
        """Test search respects limit parameter."""
        for i in range(5):
            client.post("/study", json={"topic": f"Topic {i}"})
        
        response = client.get("/interactions/search?q=Topic&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_search_requires_query(self):
        """Test search requires query parameter."""
        response = client.get("/interactions/search")
        assert response.status_code == 422  # Unprocessable Entity


class TestIntegrationFlow:
    """Test the complete flow of saving and retrieving study materials."""

    def test_full_workflow(self):
        """Test complete workflow: save, list, get, search."""
        # Save a study material
        topic = "Machine Learning"
        response = client.post("/study", json={"topic": topic})
        assert response.status_code == 200
        
        # List interactions
        response = client.get("/interactions")
        assert response.status_code == 200
        assert len(response.json()) == 1
        
        # Get specific study
        response = client.get(f"/interactions/{topic}")
        assert response.status_code == 200
        assert "summary" in response.json()
        
        # Search for study
        response = client.get("/interactions/search?q=Machine")
        assert response.status_code == 200
        assert len(response.json()) == 1