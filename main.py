from fastapi import FastAPI
from src.features.contacts import contacts_controller

app = FastAPI()

app.include_router(contacts_controller.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)