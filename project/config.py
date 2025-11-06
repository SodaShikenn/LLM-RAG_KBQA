import os

CURRENT_VERSION = '1.0.0'
DEBUG = True

# You can generate a strong key using `openssl rand -base64 42`.
SECRET_KEY = 'CAUoej9GdRX55DeVJGGOb6hTt47MWCs+AuNclM9lDeZP5v5gQZ3IAGsK'

TIMEZONE = 'Asia/Tokyo'

# PostgreSQL database config
DB_HOST = '127.0.0.1'
DB_PORT = '5432'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'vl8jhGRflh6fIeJu'
DB_DATABASE = 'llm_rag'

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# Milvus database config
MILVUS_HOST = '127.0.0.1'
MILVUS_PORT = '19530'