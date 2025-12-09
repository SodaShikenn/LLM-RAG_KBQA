# Knowledge Base Question Answering System with LLM-RAG

A comprehensive knowledge base question answering system built with Flask, leveraging Large Language Models (LLM) and Retrieval-Augmented Generation (RAG) for intelligent document-based Q&A.

## Overview

This system provides a complete solution for managing knowledge bases, processing documents, and delivering contextual answers through AI-powered retrieval and generation. The platform features user authentication, document management, segment-level content control, vector-based search, and conversational AI capabilities.

**Last Updated:** December 9, 2025
**Version:** 1.0.0
**Status:** Core CRUD operations fully implemented with English localization

## Key Features

### 1. Authentication Module

- User login and registration
- Session management and persistence
- Secure logout functionality
- Role-based access control for knowledge base management

### 2. Knowledge Base Management

- **Dataset CRUD Operations**: Create, read, update, and delete knowledge bases (datasets)
- **Document Upload**: Upload documents in multiple formats (PDF, TXT, DOCX, CSV, XLSX, MD, JSON)
- **Document Management**: View, organize, and delete uploaded documents
- **Segment Management**:
  - View all segments within a document
  - Create custom text segments manually
  - Edit segment content and ordering
  - Delete segments
  - Automatic status tracking for processing states

### 3. Text Vectorization

- **Asynchronous Processing**: Documents are processed asynchronously for optimal performance
- **Document Segmentation**: Automatic splitting of documents into semantic chunks
- **Vector Embedding**: Text segments are converted to vector embeddings
- **Milvus Integration**: Vectors are stored in Milvus vector database for efficient similarity search

### 4. Knowledge Base Question Answering

- **Context-Aware Retrieval**: Retrieve relevant document segments based on user queries
- **LLM Integration**: Large Language Models generate accurate, context-specific answers
- **Multi-KB Support**: Users can select specific knowledge bases for targeted responses

### 5. Conversation History Management

- Track and store conversation history
- Full CRUD operations on historical dialogues
- Review past interactions and insights

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

- **LLM API**: OpenAI (configurable for custom endpoints)
- **Vector Embeddings**: Supports various embedding models via Milvus

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

6. Start the Flask application:

   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:5000`

7. (Optional) Start Celery worker for background tasks:

   ```bash
   celery -A app.celery worker --loglevel=info
   ```

### Configuration

The `config.py` file contains important settings:

- **SECRET_KEY**: Session encryption key (change in production!)
- **TIMEZONE**: Application timezone (default: Asia/Tokyo)
- **UPLOAD_FOLDER**: Path for storing uploaded documents
- **ALLOWED_EXTENSIONS**: File types allowed for upload (txt, pdf, csv, docx, xlsx, md, json)
- **MAX_CONTENT_LENGTH**: Maximum file upload size (16 MB default)

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
- `status`: Processing status
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

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
5. Upload and wait for processing

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

### Form Validation

All forms use Flask-WTF with server-side validation:

- DatasetForm: Validates dataset name and description
- DocumentForm: Validates file uploads and types
- SegmentForm: Validates segment content and ordering

### Template Filters

Custom Jinja2 filters are defined in `ext_template_filter.py`:

- `document_status`: Formats document/segment status with appropriate CSS classes

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials in `config.py`
- Ensure database exists: `psql -l`

### File Upload Issues

- Check `UPLOAD_FOLDER` permissions
- Verify `MAX_CONTENT_LENGTH` setting
- Ensure file extension is in `ALLOWED_EXTENSIONS`

### Milvus Connection Issues

- Verify Milvus is running on configured port
- Check Milvus logs for errors
- Test connection with `pymilvus` client

### Redis Connection Issues

- Verify Redis is running: `redis-cli ping`
- Check Redis configuration in `config.py`
- Ensure Celery broker URL is correct

## Future Enhancements

- [ ] Implement RAG-based question answering
- [ ] Add conversation history tracking
- [ ] Implement vector search functionality
- [ ] Add batch document processing
- [ ] Enhance UI with real-time updates
- [ ] Add user role management
- [ ] Implement API authentication
- [ ] Add export/import functionality
- [ ] Enhance document preview capabilities
- [ ] Add analytics and usage statistics

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.
