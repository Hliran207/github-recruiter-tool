from fastapi import FastAPI

app = FastAPI(
    title="GitHub Project Assessment API",
    description="Assess a candidate's GitHub project using AI",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
