# exercises/security-basics/app/main.py
# L10 — Security Hardened API
#
# Run with: uvicorn app.main:app --reload  (from security-basics/ folder)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time

# TODO: Import CORSMiddleware from fastapi.middleware.cors
from fastapi.middleware.cors import CORSMiddleware

# TODO: Import the items router
from app.routers import items

app = FastAPI(title="Security Basics API")

# TODO: Add CORS middleware
# Key concept: CORS (Cross-Origin Resource Sharing) controls which web origins
# can make requests to your API from a browser.
# NEVER use allow_origins=["*"] in production — it allows any website to call
# your API with the user's cookies/credentials.
#
app.add_middleware(
CORSMiddleware,
allow_origins=["http://localhost:3000", "https://yourfrontend.com"],
allow_credentials=True,
allow_methods=["GET", "POST", "PUT", "DELETE"],
allow_headers=["Authorization", "Content-Type"],
)

# TODO: Add rate limiting middleware
# Track request counts per IP in a simple dict
# Return 429 Too Many Requests if a single IP exceeds 10 requests per minute
# Hint: use a dict like request_counts: dict[str, list[float]] = {}
# Store timestamps of requests per IP, filter to last 60 seconds
request_counts: dict[str, list[float]] = {}
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()

    timestamps = request_counts.get(client_ip, [])

    # Keep only requests from the last 60 seconds
    timestamps = [
        timestamp
        for timestamp in timestamps
        if current_time - timestamp < 60
    ]

    # Reject if this IP has already made 10 requests
    # within the last 60 seconds.
    if len(timestamps) >= 10:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"}
        )

    # Record this request
    timestamps.append(current_time)
    request_counts[client_ip] = timestamps

    # Continue to the endpoint
    response = await call_next(request)
    return response

# TODO: Include the items router
app.include_router(items.router, prefix="/items")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)