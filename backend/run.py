# run.py
from app.main import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=f"127.0.0.1", port=8000)
