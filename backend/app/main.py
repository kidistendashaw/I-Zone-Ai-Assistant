from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, documents

# Create the FastAPI app
app = FastAPI(
    title="I-Zone AI Assistant",
    description="AI assistant that answers questions about I-Zone Technologies",
    version="1.0.0"
)

# CORS — allows the Next.js frontend (port 3000) to talk to this backend (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth.router)
app.include_router(documents.router)


@app.get("/health")
def health():
    """Health check — confirms the server is running."""
    return {
        "status": "ok",
        "message": "I-Zone AI Assistant API is running"
    }
