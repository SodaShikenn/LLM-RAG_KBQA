# Knowledge Base Question Answering System with LLM-RAG

A comprehensive knowledge base question answering system built with Flask, leveraging Large Language Models (LLM) and Retrieval-Augmented Generation (RAG) for intelligent document-based Q&A.

## Overview

This system provides infrastructure for building knowledge base question answering systems using Large Language Models and Retrieval-Augmented Generation. Currently implemented features include document management, automatic text processing, vector embedding generation, and storage in Milvus vector database. The system is RAG-ready with all necessary infrastructure in place for implementing question answering functionality.

**Last Updated:** December 17, 2025
**Version:** 1.0.0
**Status:** Document Management & Vectorization System - RAG-Ready Infrastructure (QA functionality not yet implemented)

## Key Features

### ✅ Implemented Features

#### 1. Authentication Module

- User login with session-based authentication
- Hard-coded credentials for development (`admin@qq.com` / `123456`)
- Session persistence and management
- Logout functionality
- Route protection for dataset operations

#### 2. Knowledge Base Management

- **Dataset CRUD Operations**: Create, read, update, and delete knowledge bases (datasets)
- **Document Upload**: Upload documents in multiple formats (PDF, TXT, DOCX, CSV, XLSX, MD, JSON)
- **Document Management**: View, organize, and delete uploaded documents with pagination (20 per page)
- **Segment Management**:
  - View all segments within a document
  - Create custom text segments manually
  - Edit segment content and ordering (triggers re-embedding on content change)
  - Delete segments with automatic reordering
  - Automatic status tracking for processing states

#### 3. Text Vectorization & Processing

- **Asynchronous Processing**: Documents processed via Celery task queue for optimal performance
- **Multi-Format Text Extraction**: Support for PDF (PyMuPDF), DOCX (python-docx), TXT, CSV/XLSX (pandas)
- **Document Segmentation**: Automatic splitting of documents into chunks (500 characters with 100 character overlap)
- **Vector Embedding**: Text segments converted to 1536-dimensional embeddings using OpenAI `text-embedding-3-small`
- **Milvus Integration**: Vectors stored in Milvus vector database with IVF_FLAT index for efficient similarity search
- **Status Tracking**: Real-time status updates ("init" → "indexing" → "completed" or "error")

### ❌ Not Yet Implemented

#### 4. Knowledge Base Question Answering

- Context-aware retrieval API endpoint
- LLM answer generation
- RAG retrieval + generation pipeline
- Query interface and search UI
- Multi-KB query support

#### 5. Conversation History Management

- Conversation storage and tracking
- Chat interface
- Historical dialogue management
- Message persistence

## Project Architecture

```text
project/
├── app.py                       # Application entry point
├── config.py                    # Application configuration
├── helper.py                    # Utility helper functions
├── requirements.txt             # Python dependencies
│
├── apps/                        # Application modules
│   ├── auth/                    # Authentication module
│   │   ├── __init__.py          # Blueprint initialization
│   │   └── views.py             # Login, registration, logout views
│   │
│   ├── dataset/                 # Dataset (Knowledge Base) module
│   │   ├── __init__.py          # Blueprint initialization
│   │   ├── models.py            # Dataset, Document, Segment models
│   │   ├── forms.py             # WTForms for validation
│   │   └── views/               # View controllers
│   │       ├── dataset.py       # Dataset CRUD operations
│   │       ├── document.py      # Document upload and management
│   │       └── segment.py       # Segment CRUD operations
│   │
│   ├── demo/                    # Demo module
│   │   ├── __init__.py
│   │   └── views.py
│   │
│   └── templates/               # Jinja2 HTML templates
│       ├── layouts/             # Base layouts
│       ├── widgets/             # Reusable components
│       │   ├── flash_messages.html
│       │   └── pagination.html
│       ├── auth/                # Authentication templates
│       └── dataset/             # Dataset module templates
│           ├── dataset_list.html
│           ├── dataset_create.html
│           ├── dataset_edit.html
│           ├── document_list.html
│           ├── document_create.html
│           ├── segment_list.html
│           ├── segment_create.html
│           └── segment_edit.html
│
├── commands/                    # Custom Flask CLI commands
│   ├── __init__.py
│   └── hello.py
│
├── extensions/                  # Extension integrations
│   ├── ext_celery.py            # Celery for async tasks
│   ├── ext_database.py          # SQLAlchemy database
│   ├── ext_logger.py            # Application logging
│   ├── ext_migrate.py           # Flask-Migrate for DB migrations
│   ├── ext_milvus.py            # Milvus vector database
│   ├── ext_redis.py             # Redis cache and queue
│   └── ext_template_filter.py   # Custom Jinja filters
│
├── migrations/                  # Database migration files
│
├── static/                      # Static assets
│   ├── css/                     # Stylesheets (Tailwind CSS)
│   ├── js/                      # JavaScript files
│   └── images/                  # Image assets
│
├── storage/                     # Runtime storage
│   ├── files/                   # Uploaded documents
│   └── logs/                    # Application logs
│       └── app-YYYYMMDD.log
│
└── tasks/                       # Celery background tasks
    └── demo_task.py
```

## Technology Stack

### Backend

- **Framework**: Flask 3.x
- **Database**: PostgreSQL (via SQLAlchemy)
- **Vector Database**: Milvus 2.4.4 (for semantic search)
- **Cache/Message Broker**: Redis
- **Task Queue**: Celery (for asynchronous processing)
- **ORM**: Flask-SQLAlchemy
- **Migrations**: Flask-Migrate (Alembic)
- **Forms**: Flask-WTF (WTForms with CSRF protection)

### Frontend

- **Template Engine**: Jinja2
- **CSS Framework**: Tailwind CSS
- **JavaScript**: Vanilla JS
- **Icons**: Font Awesome

### Document Processing

- **PDF**: PyMuPDF (fitz)
- **DOCX**: python-docx
- **Data Files**: pandas (CSV, XLSX)
- **Text Extraction**: BeautifulSoup4

### AI/ML Integration

- **Embedding API**: OpenAI API (`text-embedding-3-small` model)
- **Vector Embeddings**: 1536-dimensional vectors stored in Milvus
- **Configurable Endpoints**: Support for custom OpenAI-compatible APIs via environment variables

### Development Tools

- **WSGI Server**: Gunicorn (production)
- **Environment Management**: python-dotenv

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Redis server
- Milvus vector database (v2.4+)

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd code/project
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application by editing `config.py`:

   ```python
   # Database configuration
   DB_HOST = '127.0.0.1'
   DB_PORT = '5432'
   DB_USERNAME = 'your_username'
   DB_PASSWORD = 'your_password'
   DB_DATABASE = 'llm_rag'

   # Milvus configuration
   MILVUS_HOST = '127.0.0.1'
   MILVUS_PORT = '19530'

   # Redis configuration
   CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
   CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
   ```

4. Create the PostgreSQL database:

   ```bash
   createdb llm_rag
   ```

5. Initialize database migrations:

   ```bash
   flask db upgrade
   ```

6. Configure environment variables (create `.env` file in project directory):

   ```bash
   OPENAI_BASE_URL=https://api.openai.com/v1
   OPENAI_API_KEY=your_openai_api_key_here
   ```

7. Start the Flask application:

   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:5000`

8. **IMPORTANT**: Start Celery worker for background document processing:

   ```bash
   celery -A app.celery worker --loglevel=info --queues=dataset
   ```

   **Note**: Document upload and vectorization will NOT work without the Celery worker running. The worker processes documents asynchronously and generates embeddings.

9. Initialize Milvus collection (first time setup):

   ```bash
   flask dataset_init_milvus
   ```

### Configuration

The `config.py` file contains important settings:

- **SECRET_KEY**: Session encryption key (change in production!)
- **TIMEZONE**: Application timezone (default: Asia/Tokyo)
- **UPLOAD_FOLDER**: Path for storing uploaded documents (`storage/files/`)
- **ALLOWED_EXTENSIONS**: File types allowed for upload (txt, pdf, csv, docx, xlsx, md, json)
- **MAX_CONTENT_LENGTH**: Maximum file upload size (16 MB default)
- **SEGMENT_LENGTH**: Text chunk size (500 characters)
- **OVERLAP**: Overlap between chunks (100 characters)
- **TOP_K**: Number of similar vectors to retrieve (3)
- **EMBEDDING_MODEL_NAME**: OpenAI embedding model (`text-embedding-3-small`)
- **OPENAI_BASE_URL**: OpenAI API base URL (configurable via .env)
- **OPENAI_API_KEY**: OpenAI API key (configurable via .env)

## Database Schema

### Dataset (Knowledge Base)

- `id`: Primary key
- `name`: Knowledge base name (max 50 chars)
- `desc`: Description (max 200 chars)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Document

- `id`: Primary key
- `dataset_id`: Foreign key to Dataset
- `file_name`: Original filename (max 100 chars)
- `file_path`: Storage path (max 100 chars)
- `status`: Processing status
- `created_at`: Upload timestamp
- `updated_at`: Last update timestamp

### Segment

- `id`: Primary key
- `dataset_id`: Foreign key to Dataset
- `document_id`: Foreign key to Document
- `order`: Segment order/position
- `content`: Text content
- `status`: Processing status ("init", "completed")
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Milvus Vector Collection

**Collection Name**: `dataset_collection`

**Schema**:

- `id`: INT64 (Primary Key, auto-increment)
- `dataset_id`: INT64 (Knowledge base identifier)
- `document_id`: INT64 (Source document identifier)
- `segment_id`: INT64 (Text segment identifier)
- `text_vector`: FLOAT_VECTOR (1536 dimensions)

**Index**: IVF_FLAT with L2 distance metric

**Operations Available**:

- `search()`: Vector similarity search with expression filtering
- `insert()`: Add new vectors with metadata
- `delete()`: Remove vectors by expression (e.g., by segment_id)
- `query()`: Retrieve vectors by metadata

## Background Tasks (Celery)

The system uses Celery for asynchronous processing of documents. Two main tasks handle the vectorization pipeline:

### 1. Dataset Document Split Task

**File**: [tasks/dataset_document_split_task.py](tasks/dataset_document_split_task.py)

**Trigger**: Automatically queued when a document is uploaded

**Process**:

1. Reads uploaded file from storage
2. Extracts text based on file format:
   - **PDF**: PyMuPDF (fitz) library
   - **DOCX**: python-docx library
   - **TXT**: Direct file read
   - **CSV/XLSX**: pandas library
3. Splits text into segments (500 char chunks with 100 char overlap)
4. Creates Segment records in database
5. Updates document status to "indexing"
6. Triggers embedding task after 10 seconds

**Queue**: `dataset`

### 2. Dataset Segment Embed Task

**File**: [tasks/dataset_segment_embed_task.py](tasks/dataset_segment_embed_task.py)

**Trigger**: Called by document split task OR when segment is manually edited

**Process**:

1. Retrieves segment content from database
2. Calls OpenAI API to generate embeddings (`text-embedding-3-small`, 1536 dimensions)
3. Stores vectors in Milvus collection with metadata:
   - `dataset_id`: Knowledge base identifier
   - `document_id`: Source document identifier
   - `segment_id`: Segment identifier
   - `text_vector`: 1536-dimensional embedding
4. Updates segment/document status to "completed"

**Queue**: `dataset`

**Modes**:

- **Batch Mode**: Processes all segments in a document
- **Single Mode**: Re-embeds a single edited segment

### Task Monitoring

View Celery worker logs in real-time:

```bash
tail -f storage/logs/celery_worker.log
```

Retry failed tasks:

```bash
flask dataset_retry_task
```

## Flask CLI Commands

Custom management commands for administrative tasks:

### Database Migrations

```bash
# Create new migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations to database
flask db upgrade

# Rollback last migration
flask db downgrade
```

### Milvus Management

```bash
# Initialize/reset Milvus collection (drops existing collection!)
flask dataset_init_milvus

# Test Milvus connection
flask test_milvus
```

### Task Debugging

```bash
# Retry failed document processing tasks
flask dataset_retry_task

# Test Celery task execution
flask test_task

# Test document splitting on specific document
flask test_dataset_document_split_task
```

## Usage

### Creating a Knowledge Base

1. Navigate to the Dataset list page
2. Click "Create New Dataset"
3. Enter a name and description
4. Submit the form

### Uploading Documents

1. Open a dataset from the list
2. Navigate to the Document list
3. Click "Upload Document"
4. Select a file (PDF, DOCX, TXT, CSV, XLSX, MD, JSON)
5. Upload - the file will be processed asynchronously

**Processing Workflow**:

1. File uploaded to `storage/files/` with UUID-based filename
2. Document record created with status "init"
3. Background task extracts text and creates segments
4. Document status changes to "indexing"
5. Another background task generates embeddings
6. Vectors stored in Milvus
7. Document status changes to "completed"

**Note**: Ensure Celery worker is running for processing to occur. Check status on the document list page.

### Managing Segments

1. From the Document list, click "View Segments" on any document
2. View all segments extracted from the document
3. Create manual segments by clicking "Insert Segment"
4. Edit segment content and order as needed
5. Delete segments that are not relevant

### Segment Operations

- **Create**: Manually add text segments with custom content and ordering
- **Edit**: Modify segment content or change display order
- **Delete**: Remove unwanted segments
- **View**: Browse all segments with status indicators

## API Endpoints

### Dataset Routes (`/dataset`)

- `GET /` - List all datasets
- `GET /dataset_create` - Show dataset creation form
- `POST /dataset_create` - Create new dataset
- `GET /dataset_edit/<int:dataset_id>` - Show dataset edit form
- `POST /dataset_edit/<int:dataset_id>` - Update dataset
- `GET /dataset_delete/<int:dataset_id>` - Delete dataset

### Document Routes (`/dataset`)

- `GET /document/<int:dataset_id>` - List documents in dataset
- `GET /document_create/<int:dataset_id>` - Show document upload form
- `POST /document_create/<int:dataset_id>` - Upload document
- `GET /document_delete/<int:document_id>` - Delete document

### Segment Routes (`/dataset`)

- `GET /segment/<int:document_id>` - List segments in document
- `GET /segment_create/<int:document_id>` - Show segment creation form
- `POST /segment_create/<int:document_id>` - Create segment
- `GET /segment_edit/<int:segment_id>` - Show segment edit form
- `POST /segment_edit/<int:segment_id>` - Update segment
- `GET /segment_delete/<int:segment_id>` - Delete segment

### Authentication Routes (`/auth`)

- `GET /login` - Show login page
- `POST /login` - Process login
- `GET /register` - Show registration page
- `POST /register` - Process registration
- `GET /logout` - Logout user

## Development Notes

### Flask Blueprints

The application uses Flask Blueprints for modular organization:

- **auth**: Handles user authentication (`/auth/*`)
- **dataset**: Manages datasets, documents, and segments (`/dataset/*`)
- **demo**: Demo routes for testing

### Database Migrations

To create a new migration after model changes:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### Helper Functions

**File**: [helper.py](helper.py)

The helper module provides utility functions for the RAG pipeline:

#### `allowed_file(filename)`

Validates uploaded file extensions against `ALLOWED_EXTENSIONS` config.

#### `segment_text(text, segment_length=500, overlap=100)`

Splits long text into overlapping chunks for better context retention.

- **Default chunk size**: 500 characters
- **Default overlap**: 100 characters
- **Returns**: List of text segments

#### `get_embedding_model()`

Returns the configured embedding model settings from `EMBEDDING_MODELS` config.

#### `get_llm_embedding(input_text)`

Calls OpenAI API to generate vector embeddings.

- **Input**: Text string or list of strings
- **Returns**: OpenAI embeddings response object
- **Model**: `text-embedding-3-small` (1536 dimensions)
- **Configurable**: Base URL and API key via environment variables

### Form Validation

All forms use Flask-WTF with server-side validation:

- **DatasetForm**: Validates dataset name (required, max 50 chars) and description (required, max 200 chars)
- **SegmentForm**: Validates segment content (required) and order (integer, required)

### Template Filters

Custom Jinja2 filters defined in [ext_template_filter.py](extensions/ext_template_filter.py):

#### `document_status` Filter

Formats document/segment status codes into display labels with CSS classes:

- `"init"` → "Initialized" (blue badge)
- `"indexing"` → "Indexing" (orange badge)
- `"error"` → "Error" (red badge)
- `"completed"` → "Completed" (green badge)

## Troubleshooting

### Documents Stuck in "init" or "indexing" Status

**Cause**: Celery worker is not running or has crashed

**Solution**:

1. Check if Celery worker is running:

   ```bash
   ps aux | grep celery
   ```

2. Check Celery worker logs:

   ```bash
   tail -f storage/logs/celery_worker.log
   ```

3. Restart Celery worker:

   ```bash
   celery -A app.celery worker --loglevel=info --queues=dataset
   ```

4. Retry failed tasks:

   ```bash
   flask dataset_retry_task
   ```

### OpenAI API Errors

**Cause**: Invalid API key or network issues

**Solution**:

1. Verify `.env` file contains valid `OPENAI_API_KEY`
2. Check API key has not expired
3. Verify `OPENAI_BASE_URL` is accessible
4. Check Celery worker logs for specific error messages

### Database Connection Issues

**Symptoms**: Application crashes on startup or database operations fail

**Solution**:

- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials in `config.py`
- Ensure database exists: `psql -l | grep llm_rag`
- Test connection: `psql -h 127.0.0.1 -U postgres -d llm_rag`

### File Upload Issues

**Symptoms**: Upload fails or returns error

**Solution**:

- Check `storage/files/` directory exists and has write permissions
- Verify `MAX_CONTENT_LENGTH` setting (default 16MB)
- Ensure file extension is in `ALLOWED_EXTENSIONS`
- Check disk space: `df -h`

### Milvus Connection Issues

**Symptoms**: Embedding task fails with Milvus errors

**Solution**:

- Verify Milvus is running: `docker ps | grep milvus` (if using Docker)
- Check Milvus is accessible on port 19530: `telnet 127.0.0.1 19530`
- Reinitialize collection: `flask dataset_init_milvus`
- Test connection: `flask test_milvus`

### Redis Connection Issues

**Symptoms**: Celery worker fails to start

**Solution**:

- Verify Redis is running: `redis-cli ping` (should return "PONG")
- Check Redis configuration in `config.py`
- Ensure Celery broker URL is correct
- Check Redis logs: `tail -f /var/log/redis/redis-server.log`

### Common Error Messages

#### "No module named 'fitz'"

Install PyMuPDF: `pip install PyMuPDF`

#### "Collection 'dataset_collection' not found"

Initialize Milvus: `flask dataset_init_milvus`

#### "Session expired" after login

- Check `SECRET_KEY` is set in `config.py`
- Clear browser cookies

## Current System Capabilities

### What Works Now

1. **Document Management Pipeline**: Upload → Extract → Segment → Embed → Store in Milvus
2. **Vector Database**: All text segments are embedded and searchable in Milvus
3. **Manual Content Management**: Full control over datasets, documents, and segments
4. **Asynchronous Processing**: Background tasks handle time-consuming operations
5. **Status Tracking**: Monitor document processing stages in real-time

### What's Missing for Complete RAG

1. **Query Endpoint**: No API to accept user questions
2. **Vector Retrieval**: Milvus search capability exists but not exposed via web interface
3. **LLM Answer Generation**: No integration with LLMs for generating responses
4. **Conversation Interface**: No chat UI or API
5. **Conversation History**: Database model was removed in migration

### RAG Implementation Roadmap

To complete the RAG question answering system:

- [ ] **Phase 1: Basic QA**
  - [ ] Create `/chat` blueprint
  - [ ] Implement question answering endpoint
  - [ ] Add vector similarity search using existing Milvus infrastructure
  - [ ] Integrate LLM for answer generation (OpenAI API or alternatives)

- [ ] **Phase 2: Conversation Management**
  - [ ] Add Conversation model back to database
  - [ ] Implement conversation history CRUD operations
  - [ ] Build chat interface UI
  - [ ] Add message persistence

- [ ] **Phase 3: Enhancements**
  - [ ] Multi-knowledge base query support
  - [ ] Streaming responses (Server-Sent Events)
  - [ ] Conversation context management
  - [ ] Retrieved context display
  - [ ] Answer source attribution

- [ ] **Phase 4: Production Features**
  - [ ] User authentication (replace hard-coded credentials)
  - [ ] API authentication (JWT tokens)
  - [ ] Rate limiting
  - [ ] Export/import functionality
  - [ ] Analytics and usage statistics
  - [ ] Document preview capabilities

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Summary

### Current State

This project implements a **RAG-ready document management and vectorization system**. It successfully handles the "Retrieval" infrastructure of RAG but lacks the "Augmented Generation" component for answering questions.

**What's Built**:

- Complete document management pipeline (upload, process, segment, vectorize)
- Asynchronous processing with Celery task queue
- Vector storage in Milvus with efficient similarity search capability
- Multi-format document support (PDF, DOCX, TXT, CSV, XLSX, MD, JSON)
- Segment-level content management with manual override capabilities
- Basic authentication and session management

**What's Missing**:

- Question answering API endpoint
- LLM integration for answer generation
- Chat/conversation interface
- Conversation history persistence
- Web UI for querying knowledge bases

### Next Steps for Developers

To complete the RAG system, implement:

1. **Chat Blueprint**: Create `/chat` routes and views
2. **Retrieval Service**: Use existing Milvus search to find relevant segments
3. **LLM Integration**: Add OpenAI Chat Completions API for answer generation
4. **UI Components**: Build chat interface with streaming responses
5. **Conversation Model**: Re-add conversation history to database

The heavy lifting (document processing, embedding, vector storage) is done. Adding the QA layer is straightforward using the existing infrastructure.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

Built with Flask, PostgreSQL, Milvus, Redis, and Celery
