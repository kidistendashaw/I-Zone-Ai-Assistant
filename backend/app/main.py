from fastapi import FastAPI

app = FastAPI(title="I-Zone AI Assistant")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "I-Zone AI Assistant API is running"
    }