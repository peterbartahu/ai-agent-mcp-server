import os
import re
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection

load_dotenv()

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin:password@localhost:27017/ai_agent_db?authSource=admin")
_client = MongoClient(MONGO_URL)
_db = _client.ai_agent_db
_interactions_collection: Collection = _db.interactions

# Create index on topic for fast lookup
_interactions_collection.create_index("topic", unique=False)


def save_interaction(topic: str, response: dict) -> dict:
    """Save an interaction to MongoDB.
    
    Args:
        topic: The study topic (key)
        response: The full response dict from /study endpoint
    
    Returns:
        The saved document with _id
    """
    doc = {
        "topic": topic,
        "response": response,
        "created_at": datetime.utcnow(),
    }
    result = _interactions_collection.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc


def get_interaction(topic: str) -> dict | None:
    """Retrieve an interaction by topic.
    
    Args:
        topic: The study topic to retrieve
    
    Returns:
        The interaction document or None if not found
    """
    doc = _interactions_collection.find_one({"topic": topic})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def list_interactions(limit: int = 100) -> list[dict]:
    """List all stored interactions.
    
    Args:
        limit: Maximum number of interactions to return
    
    Returns:
        List of interactions (without full response, just metadata)
    """
    results = []
    for doc in _interactions_collection.find().limit(limit):
        results.append({
            "id": str(doc["_id"]),
            "topic": doc.get("topic", ""),
            "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else "",
        })
    return results


def search_interactions(query: str, limit: int = 100) -> list[dict]:
    """Search interactions by topic using regex search.
    
    Args:
        query: Search query string (case-insensitive, partial match)
        limit: Maximum number of results
    
    Returns:
        List of matching interactions
    """
    results = []
    # Escape special regex characters and search case-insensitively
    escaped_query = re.escape(query)
    for doc in _interactions_collection.find(
        {"topic": {"$regex": escaped_query, "$options": "i"}}
    ).limit(limit):
        results.append({
            "id": str(doc["_id"]),
            "topic": doc.get("topic", ""),
            "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else "",
        })
    return results


def delete_interaction(topic: str) -> bool:
    """Delete an interaction by topic.
    
    Args:
        topic: The topic to delete
    
    Returns:
        True if deleted, False if not found
    """
    result = _interactions_collection.delete_one({"topic": topic})
    return result.deleted_count > 0


def clear_all() -> int:
    """Clear all interactions (useful for testing).
    
    Returns:
        Number of documents deleted
    """
    result = _interactions_collection.delete_many({})
    return result.deleted_count
