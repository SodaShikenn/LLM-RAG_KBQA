## Install Dependencies
docker-compose -f milvus-standalone-docker-compose.yml up -d
docker-compose up -d

## Environment Variables Setup
Copy .env.example to .env and fill in your API keys:
cp .env.example .env
# Edit .env file and add your OPENAI_API_KEY

## Database Migration
flask db init
flask db migrate
flask db upgrade

## Initialize Milvus
flask dataset_init_milvus

## Start Celery Worker
celery -A app.celery worker -c 2 --loglevel INFO -Q dataset --logfile storage/logs/celery_worker.log

## Start Flask Server
flask run --debug




