from fastapi import FastAPI, HTTPException, Request
from .tasks import long_running_task, get_all_tasks
import json
from bson import json_util

app = FastAPI(
    title="Celery Task API",
    description="FastAPI application with Celery task queue",
    version="1.0.0",
)


@app.post("/create-task")
async def create_task(request: Request):
    """Create a new Celery task"""
    task_input = await request.json()

    metadata_1 = task_input.pop("metadata_1", None)
    metadata_2 = task_input.pop("metadata_2", None)

    task = long_running_task.delay(
        task_input=task_input, metadata_1=metadata_1, metadata_2=metadata_2
    )

    print("kicking off a task!")
    return task.id


@app.get("/task/{task_id}")
async def get_task_result(task_id: str):
    """Get the result of a task by ID"""
    task = long_running_task.AsyncResult(task_id)
    if task.failed():
        raise HTTPException(status_code=500, detail="Task failed")

    result = None
    if task.ready():
        result = task.get()

    return {"status": task.status, "result": result}


@app.get("/tasks")
async def get_all_task_results():
    """Get all tasks and their results from the MongoDB backend"""
    tasks = get_all_tasks()
    # Convert MongoDB objects to JSON-serializable format
    return json.loads(json_util.dumps(tasks))
