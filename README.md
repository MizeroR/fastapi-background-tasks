# FastAPI Background Tasks Project

A learning project demonstrating how to implement background task processing in FastAPI. This project showcases asynchronous task execution without blocking API responses.

## Project Overview

This API implements background tasks that run after returning responses to clients. Background tasks are useful for operations like logging, analysis, file writing, or other time-consuming processes that don't need to block the user.

## Running the Project

### Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn

### Start the Server

```bash
source venv/bin/activate
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

---

## Implementation Steps

### Step 1: Task Creation & Activity Tracking

**Endpoint**: `POST /projects/{project_id}/tasks/`

**Purpose**: Create a project task and log the activity in the background

**Request Body**:

```json
{
  "task_name": "Setup database",
  "assigned_to": "Alice"
}
```

**Response**:

```json
{
  "task_id": "task_101_15",
  "status": "created"
}
```

**Background Task**:

- Logs activity to `activities.log` with timestamp
- Records: project ID, activity description, and user who performed it
- Runs asynchronously without delaying response

**Output File**: `activities.log`

```
[2026-04-16 20:17:10] Project 101: created 'Setup database' by Alice
```

---

### Step 2: Review Analysis & Sentiment Scoring

**Endpoint**: `POST /products/{product_id}/reviews`

**Purpose**: Submit a product review and perform sentiment analysis in the background

**Request Body**:

```json
{
  "customer_id": 456,
  "rating": 5,
  "review_text": "This product is amazing and excellent quality!"
}
```

**Response**:

```json
{
  "review_id": "review_789_456",
  "status": "submitted"
}
```

**Background Task**:

- Analyzes review text for positive sentiment words
- Scores based on keyword matches (great, excellent, amazing, love, perfect)
- Simulates processing time (2-second delay)
- Stores analysis result as JSON with customer ID, product ID, rating, sentiment score, and timestamp

**Output File**: `review_analysis.json`

```json
{
  "customer_id": 456,
  "product_id": 789,
  "rating": 5,
  "sentiment_score": 2,
  "analysis_timestamp": "2026-04-17T23:53:52.173400"
}
```

---

## Key Concepts

### Background Tasks Pattern

```python
background_tasks.add_task(function_name, arg1, arg2, ...)
```

- Tasks are added to a queue and executed after the response is sent
- API response is not delayed waiting for task completion
- Perfect for: logging, notifications, heavy processing, file I/O

### Data Models Used

**TaskCreate**:

- `task_name`: Name of the task
- `assigned_to`: User responsible for the task

**ReviewSubmission**:

- `customer_id`: Integer ID of customer
- `rating`: Integer rating (typically 1-5)
- `review_text`: Text content of the review

---

## Output Files

| File                   | Purpose                  | Format                     |
| ---------------------- | ------------------------ | -------------------------- |
| `activities.log`       | Timestamped activity log | Plain text, line-delimited |
| `review_analysis.json` | Analysis results         | JSON, line-delimited       |


## Development Notes

- All timestamps are captured when tasks execute (in background)
- Output files are appended to, not overwritten
- File I/O operations happen asynchronously in the background
- Sentiment analysis uses simple keyword matching (can be enhanced)

## Testing

Use a REST client (Postman, curl, VS Code REST Client) to test endpoints:

```bash
# Test Task Creation
curl -X POST "http://127.0.0.1:8000/projects/101/tasks/" \
  -H "Content-Type: application/json" \
  -d '{"task_name":"Setup database","assigned_to":"Alice"}'

# Test Review Submission
curl -X POST "http://127.0.0.1:8000/products/789/reviews" \
  -H "Content-Type: application/json" \
  -d '{"customer_id":456,"rating":5,"review_text":"This product is amazing and excellent quality!"}'
```
