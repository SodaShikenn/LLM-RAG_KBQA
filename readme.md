# Knowledge Base Question Answering System with LLM-RAG

A comprehensive knowledge base question answering system built with Flask, leveraging Large Language Models (LLM) and Retrieval-Augmented Generation (RAG) for intelligent document-based Q&A.

## Overview

This system provides a complete solution for managing knowledge bases, processing documents, and delivering contextual answers through AI-powered retrieval and generation. The platform features user authentication, document management, vector-based search, and conversational AI capabilities.

**Last Updated:** December 2, 2025
**Status:** Knowledge base CRUD operations fully implemented

## Key Features

### 1. Authentication Module

- User login and registration
- Session management and persistence
- Secure logout functionality
- Role-based access control for knowledge base management

### 2. Knowledge Base Management

- **KB CRUD Operations**: Create, read, update, and delete knowledge bases
- **Document Management**: Upload and manage documents via web interface
- **Segment Management**: Break down documents into manageable segments
- Add custom text segments to enhance knowledge base content

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
├── apps/
│   ├── auth/                    # Authentication module
│   ├── dataset/                 # Knowledge base (dataset) module
│   ├── document/                # Document management module
│   ├── segment/                 # Segment management module
│   └── demo/                    # Demo module
│       ├── __init__.py          # Blueprint initialization
│       └── views.py             # View functions
├── commands/
│   ├── __init__.py              # Custom commands initialization
│   └── hello.py                 # Example custom command
├── config.py                    # Application configuration
├── extensions/
│   ├── ext_celery.py            # Celery integration for async tasks
│   ├── ext_database.py          # Database setup and integration
│   ├── ext_logger.py            # Logging configuration
│   ├── ext_migrate.py           # Database migration setup
│   ├── ext_milvus.py            # Milvus vector database integration
│   ├── ext_redis.py             # Redis configuration
│   └── ext_template_filter.py   # Custom Jinja template filters
├── helper.py                    # Utility helper functions
├── requirements.txt             # Python dependencies
├── static/                      # Static assets (CSS, JS, images)
├── templates/                   # HTML templates
├── storage/
│   ├── files/                   # Uploaded document storage
│   └── logs/
│       └── app-YYYYMMDD.log     # Application log files
└── tasks/
    └── demo_task.py             # Background task examples
```

## Technology Stack

- **Backend Framework**: Flask
- **Database**: PostgreSQL/MySQL (via SQLAlchemy)
- **Vector Database**: Milvus
- **Cache/Queue**: Redis
- **Task Queue**: Celery
- **LLM Integration**: OpenAI API / Custom LLM endpoints
- **Frontend**: HTML, CSS (Tailwind), JavaScript

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL or MySQL
- Redis
- Milvus vector database

### Installation

1. Clone the repository

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure `config.py` with your database and API credentials

4. Initialize the database:

   ```bash
   flask db upgrade
   ```

5. Run the application:

   ```bash
   python app.py
   ```

## Usage

1. **Login**: Access the system through the authentication module
2. **Create Knowledge Base**: Set up a new KB with name and description
3. **Upload Documents**: Add documents to your knowledge base
4. **Ask Questions**: Query your knowledge base for intelligent, context-aware answers
5. **Review History**: Access past conversations and insights

## License

[Your License Here]

## Contributing

Contributions are welcome! Please submit pull requests or open issues for any improvements.
