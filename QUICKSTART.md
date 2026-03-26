# Quick Reference Guide

## Installation

```bash
# Install dependencies
poetry install

# Create .env file
cat > .env << EOF
USE_OPENAI=false
MONGO_URL=mongodb://admin:password@localhost:27017/ai_agent_db?authSource=admin
EOF
```

## Running the App

### Option 1: Quick Start Script
**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

### Option 2: Manual Steps
```bash
# Start MongoDB
docker-compose up -d

# Start server
uvicorn app.web:app --reload
```

## API Usage Examples

### 1. Generate Study Material
```bash
curl -X 'POST' 'http://localhost:8000/study' \
  -H 'Content-Type: application/json' \
  -d '{"topic": "Python"}'
```

### 2. List All Materials
```bash
curl -X 'GET' 'http://localhost:8000/interactions'
```

### 3. Get Specific Material
```bash
curl -X 'GET' 'http://localhost:8000/interactions/Python'
```

### 4. Search Materials
```bash
curl -X 'GET' 'http://localhost:8000/interactions/search?q=Python'
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test class
pytest tests/api/test_api.py::TestSearchEndpoint -v

# Run with coverage
pytest tests/ --cov=app
```

## Troubleshooting

**MongoDB not starting?**
```bash
# Check if port 27017 is in use
netstat -an | grep 27017

# Force stop existing containers
docker-compose down
docker-compose up -d
```

**Port 8000 already in use?**
```bash
# Use a different port
uvicorn app.web:app --port 8001
```

**Tests failing?**
```bash
# Make sure you're in the venv
poetry shell
pytest tests/
```

## Useful URLs

- **API Root**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **MongoDB**: mongodb://localhost:27017 (admin:password)

## Environment Variables

```bash
# LLM Configuration (optional)
USE_OPENAI=false                          # false = offline, true = OpenAI
# OPENAI_API_KEY=sk-xxxxxxxxxx           # Uncomment if USE_OPENAI=true
# OPENAI_MODEL=gpt-3.5-turbo             # Uncomment for specific model

# MongoDB Configuration (optional)
MONGO_URL=mongodb://admin:password@localhost:27017/ai_agent_db?authSource=admin
```

## Project Structure

```
app/
├── web.py                    # FastAPI app entry point
├── main.py                   # LLM factory function
├── agent/                    # Agent orchestration
├── api/study.py              # All API endpoints
├── storage/mongodb_store.py  # Database layer
├── tools/                    # Agent tools
├── export/                   # PDF export
├── rag/                      # RAG/embeddings
└── domain/                   # Data models
```

## Next Steps

1. ✅ Read `README.md` for full documentation
2. ✅ Open Swagger UI: http://localhost:8000/docs
3. ✅ Make your first request via curl or Swagger
4. ✅ Run tests: `pytest tests/`
5. ✅ Check MongoDB: `docker exec ai_agent_mongodb mongosh -u admin -p password`

## Getting Help

- 📖 Full documentation: `README.md`
- 🧪 Test examples: `tests/api/test_api.py`
- 🔧 API reference: Swagger UI at `/docs`
- 💾 Storage: `app/storage/mongodb_store.py`
