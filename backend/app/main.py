from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# This creates the FastAPI application
app = FastAPI(
    title="I-Zone AI Assistant",
    description="AI assistant that answers questions about I-Zone Technologies",
    version="1.0.0"
)

# CORS middleware — this allows the Next.js frontend to talk to this backend.
# Without this, the browser blocks all requests from the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js runs on port 3000
    allow_credentials=True,
    allow_methods=["*"],   # Allow GET, POST, PUT, DELETE etc.
    allow_headers=["*"],   # Allow all headers
)


@app.get("/health")
def health():
    """
    Health check endpoint.
    Used to confirm the backend is running.
    Visit: http://localhost:8000/health
    """
    return {
        "status": "ok",
        "message": "I-Zone AI Assistant API is running"
    }
