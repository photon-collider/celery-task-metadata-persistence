from celery import Celery
from celery.signals import before_task_publish
import time
import os
from datetime import datetime
import app.custom_backend

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
MONGODB_HOST = os.environ.get(
    "MONGODB_HOST", "mongodb://localhost:27017/celery_result_db"
)

# backend_instance = CustomBackend(
#     url='mongodb://localhost:27017/',
#     db="tasks",
#     collection="task_results"
# )


celery_app = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend="app.custom_backend.CustomBackend",
    task_track_started=True,
    mongodb_backend_settings={
        "host": MONGODB_HOST,
        "database": "tasks",
        "taskmeta_collection": "task_results",
    },
)


# celery_app.conf.update(
#     CELERY_RESULT_BACKEND="app.custom_backend.CustomBackend",
#     MONGODB_BACKEND_SETTINGS={},
# )

# celery_app.conf.result_backend_transport_options = {
#     "backend_class": "app.custom_backend.CustomBackend"
# }


@before_task_publish.connect
def on_task_publish(headers=None, body=None, exchange=None, routing_key=None, **kwargs):
    """Signal handler to store task metadata when a task is published."""
    task_id = headers.get("id")

    # Body structure is (args, kwargs, embedding)
    task_args, task_kwargs, _ = body

    meta = {
        "metadata_1": task_kwargs.get("metadata_1"),
        "metadata_2": task_kwargs.get("metadata_2"),
    }

    celery_app.backend.collection.insert_one(
        {
            "_id": task_id,
            "metadata": meta,
            "status": "QUEUED",
            "result": None,
            "traceback": None,
            "children": [],
        }
    )


@celery_app.task
def long_running_task(task_input, metadata_1=None, metadata_2=None):
    """
    A sample task that simulates long-running operation
    by sleeping for 30 seconds and returns provided kwargs
    """
    time.sleep(30)
    return f"Task completed after 30 seconds with kwargs: {task_input}"


def get_all_tasks():
    """
    Get all tasks from the MongoDB backend
    """
    collection = celery_app.backend.collection
    return list(collection.find({}))
