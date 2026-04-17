from fastapi import FastAPI, BackgroundTasks
from datetime import datetime
from pydantic import BaseModel
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI Background Tasks API", "status": "running"}

class TaskCreate(BaseModel):
    task_name: str
    assigned_to: str

class ReviewSubmission(BaseModel):
    customer_id: int
    rating: int
    review_text: str

def track_activity(project_id: int, activity: str, user: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Project {project_id}: {activity} by {user}\n"

    with open("activities.log", "a") as f:
        f.write(log_entry)
    print(f"Tracked: {activity}")

def analyze_review(customer_id: int, product_id: int, rating: int, review_text: str):
    import time
    time.sleep(2)

    positive_words = ["great", "excellent", "amazing", "love", "perfect"]
    sentiment_score = sum(1 for word in positive_words if word in review_text.lower())

    analysis_result = {
        "customer_id": customer_id,
        "product_id": product_id,
        "rating": rating,
        "sentiment_score": sentiment_score,
        "analysis_timestamp": datetime.now().isoformat(),
    }

    with open("review_analysis.json", "a") as f:
        f.write(json.dumps(analysis_result) + "\n")

    print(f"Analyzed review: {rating}/5 stars, sentiment: {sentiment_score}")

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

@app.post("/products/{product_id}/reviews")
def submit_review(
    product_id: int, 
    review_data: ReviewSubmission, 
    background_tasks: BackgroundTasks
):
    review_id = f"review_{product_id}_{review_data.customer_id}"

    background_tasks.add_task(
        analyze_review, 
        review_data.customer_id, 
        product_id, 
        review_data.rating, 
        review_data.review_text
    )

    return {"review_id": review_id, "status": "submitted"}