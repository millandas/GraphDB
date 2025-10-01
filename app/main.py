from fastapi import FastAPI

app = FastAPI(title="E-Commerce Graph API")

@app.get("/")
def read_root() -> dict:
    return {"status": "ok", "service": "api"}

@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}