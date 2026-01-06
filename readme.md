# Knowledge Base Question Answering System with LLM-RAG

> **[日本語版 README はこちら](readme_ja.md)**

A production-ready RAG system built with Flask for intelligent document-based Q&A using LLMs.

**Version:** 2.0.0 | **Updated:** January 6, 2026 | **Status:** Production-Ready

## Overview

Complete RAG-based knowledge base system with document management, vector search (Milvus), multi-LLM support (OpenAI, Qwen), streaming responses, and conversation history.

## Key Features

- **RAG Pipeline**: Full retrieval-augmented generation with vector similarity search (Milvus) + LLM completion
- **Multi-Format Documents**: PDF, DOCX, TXT, CSV, XLSX, MD, JSON with automatic text extraction
- **Vector Embeddings**: OpenAI text-embedding-3-small (1536-dim) with IVF_FLAT indexing
- **Multiple LLMs**: OpenAI gpt-4o-mini & Alibaba Qwen qwen-max support
- **Streaming Responses**: Real-time LLM output with Server-Sent Events
- **Conversation Management**: Full CRUD with persistent history (JSON storage)
- **Async Processing**: Celery + Redis for background document vectorization
- **Interactive UI**: Alpine.js + Tailwind CSS chat interface with markdown rendering
- **Multi-KB Queries**: Query across multiple knowledge bases simultaneously
- **Manual Overrides**: Edit segments and trigger re-embedding on demand

## Architecture

```text
project/
├── app.py, config.py, helper.py
├── apps/
│   ├── auth/          # Session-based authentication
│   ├── chat/          # RAG Q&A + conversation management
│   ├── dataset/       # Knowledge base CRUD + document/segment management
│   └── templates/     # Jinja2 templates (chat, dataset, auth)
├── extensions/        # Celery, SQLAlchemy, Milvus, Redis, migrations
├── tasks/             # Background jobs (document splitting, embedding)
├── static/            # CSS (Tailwind), JS (Alpine.js)
└── storage/           # Uploaded files + logs
```

## System Workflow

### Document Processing Flow

```text
User Upload → File Storage → Celery Task Queue
                                    ↓
                            Text Extraction (PDF/DOCX/TXT/CSV/XLSX)
                                    ↓
                            Document Segmentation (500 chars, 100 overlap)
                                    ↓
                            Segment Storage (PostgreSQL)
                                    ↓
                            Embedding Generation (OpenAI text-embedding-3-small)
                                    ↓
                            Vector Storage (Milvus 1536-dim vectors)
                                    ↓
                            Status Update (completed)
```

### RAG Question Answering Flow

```text
User Question → Conversation Context (last 3 messages)
                        ↓
                Embedding Generation (OpenAI)
                        ↓
                Vector Similarity Search (Milvus TOP_K=3)
                        ↓
                Filter by Selected Datasets
                        ↓
                Retrieve Segment Content (PostgreSQL)
                        ↓
                Augment Prompt with Retrieved Context
                        ↓
                LLM Generation (gpt-4o-mini / qwen-max)
                        ↓
                Stream Response to User
                        ↓
                Save to Conversation History
```

## Tech Stack

**Backend**: Flask 3.x | PostgreSQL (SQLAlchemy) | Milvus 2.4.4 | Redis | Celery | Gunicorn
**Frontend**: Jinja2 | Tailwind CSS | Alpine.js | Marked.js | Font Awesome
**Document Processing**: PyMuPDF | python-docx | pandas | BeautifulSoup4
**AI/ML**: OpenAI API (text-embedding-3-small, gpt-4o-mini) | Qwen API (qwen-max)

## Quick Start

**Prerequisites**: Python 3.8+, PostgreSQL, Redis, Milvus 2.4+, OpenAI/Qwen API key

```bash
# 1. Install & setup
pip install -r requirements.txt
createdb llm_rag
flask db upgrade
flask dataset_init_milvus

# 2. Configure (edit config.py + create .env)
echo "OPENAI_API_KEY=your_key" > .env
echo "QWEN_API_KEY=your_key" >> .env

# 3. Start services (2 terminals)
python app.py                                                   # Terminal 1
celery -A app.celery worker --loglevel=info --queues=dataset   # Terminal 2

# 4. Access
# Chat: http://localhost:5000/chat
# Datasets: http://localhost:5000/dataset
# Login: admin@qq.com / 123456
```

### Key Configuration (`config.py` + `.env`)

- **Database**: PostgreSQL connection (DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_DATABASE)
- **Milvus**: Vector DB connection (MILVUS_HOST, MILVUS_PORT)
- **Redis**: Celery broker (CELERY_BROKER_URL, CELERY_RESULT_BACKEND)
- **API Keys**: OPENAI_API_KEY, QWEN_API_KEY (in `.env`)
- **RAG Config**: SEGMENT_LENGTH=500, OVERLAP=100, TOP_K=3
- **Upload**: MAX_CONTENT_LENGTH=16MB, ALLOWED_EXTENSIONS={txt,pdf,docx,csv,xlsx,md,json}

## Database Schema

**PostgreSQL Tables**:

- **Dataset**: Knowledge bases (id, name, desc, timestamps)
- **Document**: Uploaded files (id, dataset_id, file_name, file_path, status, timestamps)
- **Segment**: Text chunks (id, dataset_id, document_id, order, content, status, timestamps)
- **Conversation**: Chat history (id, uid, name, messages[JSON], timestamps)

**Milvus Collection** (`dataset_collection`):

- Schema: id, dataset_id, document_id, segment_id, text_vector[1536-dim FLOAT]
- Index: IVF_FLAT with L2 distance
- Operations: search, insert, delete, query with expression filtering

## Celery Tasks & CLI Commands

**Background Tasks** (queue: `dataset`):

1. **document_split_task**: Upload → Text extraction → Segmentation (500 chars, 100 overlap) → DB insert
2. **segment_embed_task**: Generate embeddings → Store in Milvus → Update status

**Flask Commands**:

```bash
flask db migrate/upgrade/downgrade  # DB migrations
flask dataset_init_milvus           # Initialize Milvus collection
flask dataset_retry_task            # Retry failed tasks
flask test_milvus                   # Test Milvus connection
tail -f storage/logs/celery_worker.log  # Monitor Celery logs
```

## Usage

**Knowledge Base**: Create dataset → Upload documents (auto-processed) → View/edit segments

**Chat Interface** (`/chat`):

1. Select LLM model (gpt-4o-mini / qwen-max) & knowledge bases
2. Type questions → Get streaming RAG responses
3. Manage conversations (create, rename, delete, switch)
4. RAG retrieves TOP_K=3 relevant segments when KBs selected

**Features**: Markdown rendering, conversation context, cancel requests, auto-save

## API Endpoints

- **`/auth`**: login, register, logout
- **`/dataset`**: Dataset/Document/Segment CRUD operations
- **`/chat`**: Chat UI, RAG completions (streaming), conversation CRUD, message persistence

## Key Implementation Details

**Blueprints**: auth, chat, dataset modules with separate routing

**RAG Pipeline** ([apps/chat/services.py](apps/chat/services.py)):
`retrieve_related_texts()` → Embed last 3 messages → Milvus search (TOP_K=3) → Filter by dataset_ids → Inject segments as system message

**Helper Functions** ([helper.py](helper.py)):
`get_llm_embedding()`, `get_llm_chat()`, `segment_text()`, `json_response()`

**Status Filter**: init → indexing → completed / error (color-coded badges)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Docs stuck in "init"/"indexing"** | Start Celery worker: `celery -A app.celery worker --loglevel=info --queues=dataset` |
| **OpenAI API errors** | Check `.env` has valid `OPENAI_API_KEY`, verify API key not expired |
| **DB connection fails** | Verify PostgreSQL running: `sudo systemctl status postgresql`, check `config.py` credentials |
| **Upload fails** | Check `storage/files/` permissions, verify file extension allowed, check disk space |
| **Milvus errors** | Test connection: `flask test_milvus`, reinitialize: `flask dataset_init_milvus` |
| **Celery won't start** | Verify Redis: `redis-cli ping` should return "PONG" |
| **"No module named 'fitz'"** | Install: `pip install PyMuPDF` |

## Production Enhancements

Optional features for production deployment:

- User authentication & authorization
- API rate limiting & JWT tokens
- Monitoring, logging, backup/recovery
- Load balancing & caching
- Source attribution in answers
- Hybrid search (vector + keyword)
- Multi-tenancy support

## License & Contributing

MIT License | Contributions welcome via Pull Requests

**Built with**: Flask | PostgreSQL | Milvus | Redis | Celery | OpenAI
