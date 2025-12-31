from fastapi import FastAPI
from queue import Queue
import threading
import time
import uuid

app = FastAPI()

# Queue create
task_queue = Queue()

# Background worker function
def worker():
    while True:
        task = task_queue.get()
        if task is None:
            break

        print(f"Processing task: {task['task_id']}")
        time.sleep(5)  # heavy work simulation
        print(f"Task completed: {task['task_id']}")

        task_queue.task_done()

# Start background worker thread
threading.Thread(target=worker, daemon=True).start()

# API endpoint to add task to queue
@app.post("/add-task")
def add_task(data: dict):
    task_id = str(uuid.uuid4())

    task = {
        "task_id": task_id,
        "payload": data
    }

    task_queue.put(task)

    return {
        "message": "Task queue mein add ho gaya",
        "task_id": task_id
    }

# Health check
@app.get("/")
def home():
    return {"status": "Web service running with queue"}