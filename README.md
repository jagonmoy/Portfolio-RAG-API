# Portfolio RAG API

A FastAPI-based RAG (Retrieval-Augmented Generation) service that answers questions about Jagonmoy Dey's professional background using LlamaIndex and ChromaDB.

## Features

- 🚀 FastAPI backend with async support
- 🔍 RAG implementation using LlamaIndex
- 💾 ChromaDB for vector storage (file-based for free hosting)
- 📄 PDF and text document processing
- 🐙 GitHub repository analysis
- 🌐 Portfolio website content extraction
- 📊 Structured logging and error handling
- 🚢 Ready for Railway/Render deployment

## Quick Start

```bash
# 1. Setup (installs uv + dependencies)
./scripts/dev.sh setup

# 2. Add your OPENAI_API_KEY to .env file

# 3. Start development server
./scripts/dev.sh
```

### Commands
```bash
./scripts/dev.sh setup    # Setup project
./scripts/dev.sh          # Start dev server  
./scripts/dev.sh test     # Run validation
uv add package-name       # Add dependency
```

## API Endpoints

### Core Query Endpoint
```http
POST /api/v1/query
Content-Type: application/json

{
  "question": "What is Jagonmoy's experience with React?",
  "max_tokens": 200,
  "temperature": 0.1
}
```

### Document Management
```http
# Upload document
POST /api/v1/documents/upload

# Process GitHub repository
POST /api/v1/documents/github?repo_url=https://github.com/user/repo

# Process portfolio website
POST /api/v1/documents/portfolio?url=https://jagonmoy.github.io
```

### Health Check
```http
GET /health
GET /api/v1/documents/count
```

## Project Structure

```
Portfolio-bot/
├── app/
│   ├── api/           # FastAPI routes
│   ├── core/          # Configuration and logging
│   ├── models/        # Pydantic schemas
│   └── services/      # Business logic
├── data/
│   ├── documents/     # Source documents
│   └── storage/       # ChromaDB storage
├── tests/             # Test files
├── pyproject.toml     # Dependencies (modern Python packaging)
├── Dockerfile         # Container configuration
├── railway.json       # Railway deployment config
└── render.yaml        # Render deployment config
```


## Deployment

### Railway
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard  
3. Deploy automatically from main branch (uses Docker with uv)

### Render
1. Connect repository to Render
2. Use `render.yaml` for configuration (includes uv installation)
3. Set environment variables in Render dashboard

### Docker
```bash
# Build with uv optimization
docker build -t portfolio-rag-api .
docker run -p 8000:8000 --env-file .env portfolio-rag-api
```

## Usage

Upload documents and query your professional background via the API endpoints.

## Configuration

Add your `OPENAI_API_KEY` to `.env` file. Other settings are in `app/core/config.py`.