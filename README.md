# Celery Task Metadata Persistence


A tutorial demonstrating how to build a FastAPI application with Celery for asynchronous task processing. This demo showcases how to use Redis as a message broker and implement a custom MongoDB backend to preserve task metadata. Perfect for learning how to handle long-running tasks in FastAPI while maintaining additional task information.

This demo complements my blog post about using custom MongoDB backends with Celery.

## Table of Contents
- [Celery Task Metadata Persistence](#celery-task-metadata-persistence)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Quick Start with Docker](#quick-start-with-docker)
  - [API Endpoints](#api-endpoints)
  - [Tutorial](#tutorial)
  - [Running Locally](#running-locally)
  - [Project Structure](#project-structure)
  - [Notes](#notes)

## Prerequisites

- Docker and Docker Compose
- Python 3.12 (if running locally)

## Quick Start with Docker

1. Clone the repository:
```bash
git clone git@github.com:photon-collider/celery-task-metadata-persistence.git
cd celery-task-metadata-persistence
```

2. Start the services using Docker Compose:
```bash
docker compose up -d
```

This will start all required services:
- FastAPI application (accessible at http://localhost:8000)
- Celery worker
- Redis broker
- MongoDB backend

## API Endpoints

- `POST /create-task`: Create a new task with optional metadata
- `GET /task/{task_id}`: Get status and result of a specific task
- `GET /tasks`: List all tasks and their current status

## Tutorial

Try out the custom MongoDB backend by creating a task with metadata:

1. Create a task with metadata:
```bash
curl -X POST http://localhost:8000/create-task \
  -H "Content-Type: application/json" \
  -d '{
    "task_input": "test task",
    "metadata_1": "important info",
    "metadata_2": "more info"
  }'
```

2. Copy the task ID from the response and check its status:
```bash
curl http://localhost:8000/task/<task-id>
```

The application uses a custom MongoDB backend for Celery to store additional metadata with task results. Tasks will take 30 seconds to complete by default (simulating long-running operations).

3. List all tasks to see the metadata:
```bash
curl http://localhost:8000/tasks
```

Notice how the metadata fields (`metadata_1` and `metadata_2`) are preserved in MongoDB even after the task completes. This demonstrates the custom backend's ability to maintain additional task information throughout the task lifecycle.

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export CELERY_BROKER_URL="redis://localhost:6379/0"
export MONGODB_HOST="mongodb://localhost:27017/celery_result_db"
```

3. Start the FastAPI application:
```bash
uvicorn app.main:app --reload --port 8000
```

4. Start the Celery worker:
```bash
celery -A app.tasks worker --loglevel=INFO -c 1
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── custom_backend.py  # Custom MongoDB backend for Celery
│   ├── main.py           # FastAPI application
│   └── tasks.py          # Celery tasks definitions
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```


## Notes

- The Celery worker is configured to run with a single concurrent process (-c 1)
- MongoDB data is persisted using a Docker volume
- The application includes health checks for both Redis and MongoDB services