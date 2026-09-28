# exercises/background-tasks/app/routers/reports.py
# L9 — Report and notification endpoints with background tasks

import time
import uuid
from typing import Optional

# TODO: Import APIRouter, BackgroundTasks from fastapi
from fastapi import APIRouter, BackgroundTasks, HTTPException  

router = APIRouter()

# In-memory store for report statuses
# Key: report_id (str), Value: dict with status and result
report_store: dict[str, dict] = {}


# ── Background task functions ─────────────────────────────────────────────────
# These are regular Python functions, not endpoints.
# FastAPI runs them in a thread pool after the response has been sent.

# TODO: Implement generate_report(report_id, report_type, rows)
# 1. Update report_store[report_id] = {"status": "processing", ...}
# 2. time.sleep(2) to simulate work
# 3. Update store to {"status": "complete", "result": {...}}
def generate_report(report_id: str, report_type: str, rows: int) -> None:
    """
    Simulates a long-running report generation task.

    TODO:
    1. Set status to "processing" in report_store
    2. time.sleep(2) — simulate work
    3. Set status to "complete" with a fake result dict
    """
    report_store[report_id] = {"status": "processing"}
    time.sleep(2)
    report_store[report_id] = {
    "status": "complete",
    "result": {
        "report_type": report_type,
        "rows": rows,
    },
}




# TODO: Implement send_notification(recipient, message)
# 1. time.sleep(1) — simulate email/SMS sending
# 2. Print a confirmation (or store in a log dict)
def send_notification(recipient: str, message: str) -> None:
    """Simulates sending a notification (email/SMS) in the background."""
    time.sleep(1)

    print(f"Notification Complete: {recipient} - {message}")


# ── Endpoints ──────────────────────────────────────────────────────────────────

# TODO: POST /reports — kick off background report generation
# Accept JSON body with report_type (str) and rows (int, default 100)
# Key concept: BackgroundTasks is injected by FastAPI.
# Call background_tasks.add_task(fn, arg1, arg2) to schedule work.
# The endpoint returns IMMEDIATELY — the response goes back to the client
# while the background task runs.
@router.post("/")
def create_report(background_tasks: BackgroundTasks, report_type: str = "sales", rows: int = 100):
    """
    Kicks off report generation and returns immediately with a report_id.

    TODO:
    1. Generate a unique report_id (use uuid.uuid4())
    2. Store initial status: report_store[report_id] = {"status": "pending"}
    3. background_tasks.add_task(generate_report, report_id, report_type, rows)
    4. Return {"report_id": report_id, "status": "pending"}

    Key concept: When to use background tasks vs async endpoints:
    - Use background tasks for work that can happen AFTER the response is sent
      (e.g., sending emails, generating files, logging, webhooks)
    - Use async def for I/O that should complete BEFORE returning a response
      (e.g., fetching data needed in the response)
    """
    report_id = str(uuid.uuid4())

    report_store[report_id] = {"status": "pending"}

    background_tasks.add_task(
        generate_report,
        report_id,
        report_type,
        rows,
    )
    return {
        "report_id": report_id,
        "status": "pending",
    }

# TODO: GET /reports/{report_id} — check report status
@router.get("/{report_id}")
def get_report_status(report_id: str):
    """
    Returns the current status of a report: pending, processing, or complete.

    TODO: Look up report_id in report_store, return 404 if not found.
    """
    if report_id not in report_store:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return report_store[report_id]
    


# TODO: POST /notifications — send a notification in the background
@router.post("/notifications")
def send_notification_endpoint(
    background_tasks: BackgroundTasks,
    recipient: str = "user@example.com",
    message: str = "Hello!",
):
    """
    Queues a notification to be sent in the background.

    TODO: add_task(send_notification, recipient, message), return immediately.
    """

    background_tasks.add_task(
        send_notification,
        recipient,
        message,
    )

    return {
        "status": "queued"
    }
