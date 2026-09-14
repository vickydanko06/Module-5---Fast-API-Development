# exercises/validated-contacts/app/main.py
# L3 — Validated Contact Book
#
# Run with: uvicorn app.main:app --reload  (from validated-contacts/ folder)

from fastapi import FastAPI
from app.routers import contacts

# TODO: Import the contacts router
# Hint: from app.routers import contacts  OR  from app.routers.contacts import router

app = FastAPI(title="Contact Book API")

app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

# TODO: Include the contacts router with prefix="/contacts" and tags=["contacts"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)