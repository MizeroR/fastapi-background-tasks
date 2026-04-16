from fastapi import FastAPI, BackgroundTasks
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI Background Tasks API", "status": "running"}

class TaskCreate(BaseModel):
    task_name: str
    assigned_to: str

def track_activity(project_id: int, activity: str, user: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Project {project_id}: {activity} by {user}\n"

    with open("activities.log", "a") as f:
        f.write(log_entry)
    print(f"Tracked: {activity}")

@app.post("/projects/{project_id}/tasks/")
def create_task(
    project_id: int, task_data: TaskCreate, background_tasks: BackgroundTasks
):
    task_id = f"task_{project_id}_{len(task_data.task_name)}"

    background_tasks.add_task(
        track_activity,
        project_id,
        f"created '{task_data.task_name}'",
        task_data.assigned_to,
    )

    return {"task_id": task_id, "status": "created"}