# AI Study Helper Agent

A modern Python-based AI Study Helper agent, built with **FastAPI** and **MongoDB**. Generate comprehensive study materials with summaries, key points, questions, and answers for any topic.

---

## Key Features

- **REST API** – FastAPI endpoints for generating and retrieving study materials
- **MongoDB Storage** – Persistent key-value storage for study interactions (key: topic, value: response)
- **Full-text Search** – Search stored study materials by topic (partial/case-insensitive)
- **LLM Abstraction** – Supports both **FakeLLM** (offline) and **OpenAI LLM** (real AI)
- **Agent Architecture** – Orchestrated tool-based flow for generating study content
- **Docker Support** – MongoDB containerized with Docker Compose
- **Comprehensive Tests** – Full test coverage for API endpoints and storage layer

---

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (for MongoDB)
- Poetry (for dependency management)

### 1. Setup

Clone the repository and install dependencies:

```bash
poetry install
```

### 2. Configure .env

Create a `.env` file in the root directory:

```bash
# LLM Configuration
USE_OPENAI=false                    # Use 'true' for OpenAI, 'false' for offline mode
# OPENAI_API_KEY=sk-xxxxxxxx       # Uncomment and add your key if USE_OPENAI=true
# OPENAI_MODEL=gpt-3.5-turbo       # Specify model (optional)

# MongoDB Configuration
MONGO_URL=mongodb://admin:password@localhost:27017/ai_agent_db?authSource=admin
```

### 3. Start MongoDB

```bash
docker-compose up -d
```

This starts MongoDB on `localhost:27017` with credentials: `admin:password`

### 4. Run the Server

```bash
uvicorn app.web:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**Swagger UI** (Interactive API documentation): `http://localhost:8000/docs`

---

## API Endpoints

### 1. Generate Study Material

**POST** `/study`

Generate study material for a topic and save to MongoDB.

```bash
curl -X 'POST' 'http://localhost:8000/study' \
  -H 'Content-Type: application/json' \
  -d '{"topic": "What is AWS S3?"}'
```

**Response:**
```json
{
  "summary": "AWS S3 is a cloud storage service...",
  "key_points": ["Point 1", "Point 2", ...],
  "questions": ["Q1", "Q2", ...],
  "answers": ["A1", "A2", ...]
}
```

---

### 2. List All Study Materials

**GET** `/interactions`

List all stored study materials (with limit support).

```bash
curl -X 'GET' 'http://localhost:8000/interactions?limit=100'
```

**Response:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "topic": "What is AWS S3?",
    "created_at": "2026-03-25T17:22:10.123456"
  }
]
```

---

### 3. Retrieve Specific Study Material

**GET** `/interactions/{topic}`

Retrieve full study material by exact topic match.

```bash
curl -X 'GET' 'http://localhost:8000/interactions/What%20is%20AWS%20S3?'
```

**Response:**
```json
{
  "summary": "AWS S3 is a cloud storage service...",
  "key_points": [...],
  "questions": [...],
  "answers": [...]
}
```

---

### 4. Search Study Materials

**GET** `/interactions/search`

Search stored study materials by topic (partial match, case-insensitive).

```bash
curl -X 'GET' 'http://localhost:8000/interactions/search?q=AWS&limit=10'
```

**Response:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "topic": "What is AWS S3?",
    "created_at": "2026-03-25T17:22:10.123456"
  }
]
```

---

## Storage Architecture

### MongoDB Collections

Data is stored in MongoDB with the following structure:

```javascript
db.interactions.insertOne({
  _id: ObjectId("..."),
  topic: "What is AWS S3?",           // Key for search/retrieval
  response: {
    summary: "...",
    key_points: [...],
    questions: [...],
    answers: [...]
  },
  created_at: ISODate("2026-03-25T17:22:10.123456Z")
})
```

### Data Flow

1. **POST /study** → Generate content via Agent → Save to MongoDB
2. **GET /interactions** → Fetch all from MongoDB
3. **GET /interactions/{topic}** → Exact match lookup in MongoDB
4. **GET /interactions/search** → Regex search in MongoDB (case-insensitive)

---

## Running Tests

Run the comprehensive test suite:

```bash
pytest tests/ -v
```

**Test Coverage:**
- Study endpoint (valid/empty topics, edge cases)
- List endpoint (empty, single, multiple items, limit)
- Get endpoint (existing, non-existent, special characters)
- Search endpoint (exact match, partial match, case-insensitive, limits)
- Full integration workflow

---

## Project Structure

```
app/
├── agent/              # Core agent and planner logic
│   ├── agent.py
│   ├── planner.py
│   ├── llm_fake.py     # Offline LLM mock
│   └── llm_openai.py   # OpenAI LLM integration
├── api/
│   └── study.py        # FastAPI endpoints
├── storage/
│   └── mongodb_store.py # MongoDB integration
├── tools/              # Agent tools (summary, questions, answers)
│   ├── summary_tool.py
│   ├── question_tool.py
│   └── answer_tool.py
├── export/
│   └── pdf_exporter.py # PDF export utility
├── rag/                # RAG/embeddings (optional)
├── domain/             # Data models
│   └── study_material.py
├── main.py             # LLM factory
└── web.py              # FastAPI app entry point
```

---

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `USE_OPENAI` | Use OpenAI LLM instead of offline | `false` | No |
| `OPENAI_API_KEY` | Your OpenAI API key | - | Only if `USE_OPENAI=true` |
| `OPENAI_MODEL` | OpenAI model name | `gpt-3.5-turbo` | No |
| `MONGO_URL` | MongoDB connection string | `mongodb://admin:password@localhost:27017/ai_agent_db?authSource=admin` | No |

---

## Development & Offline Mode

**FakeLLM** (default) generates realistic study material **without API calls**, perfect for:
- Local development
- Testing
- Demos without requiring API keys

Just keep `USE_OPENAI=false` in `.env`

---

## Using OpenAI

To enable real AI responses:

1. Set `USE_OPENAI=true` in `.env`
2. Add your OpenAI API key: `OPENAI_API_KEY=sk-xxxxxxxx`
3. (Optional) Specify model: `OPENAI_MODEL=gpt-3.5-turbo`

---

## Docker Compose Services

The `docker-compose.yml` includes:

- **MongoDB 7.0** – Database for storing interactions
  - Port: `27017`
  - Username: `admin`
  - Password: `password`
  - Database: `ai_agent_db`

---

## Future Enhancements

- [ ] User authentication & authorization
- [ ] Study material versioning
- [ ] Batch topic processing
- [ ] PDF export endpoint
- [ ] Custom prompts per tool
- [ ] Rate limiting

---

## License

MIT License - see LICENSE file for details

---

**Questions or Issues?** Open an issue on GitHub!