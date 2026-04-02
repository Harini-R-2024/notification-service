import threading
from fastapi import FastAPI
from app.database import engine, Base
import app.models.notification_model
from app.routes import notification_routes
from app.workers.worker import process_notifications

app = FastAPI(title="Notification Service")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(notification_routes.router)


@app.on_event("startup")
def start_worker():
    print("🚀 Starting background worker...")

    thread = threading.Thread(target=process_notifications, daemon=True)
    thread.start()


@app.get("/")
def root():
    return {"message": "Notification Service is running 🚀"}