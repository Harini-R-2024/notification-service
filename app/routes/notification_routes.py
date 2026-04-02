from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.notification_model import Notification, UserPreference
from app.schemas.notification_schema import NotificationCreate
from app.schemas.user_schema import UserPreferenceCreate
from app.workers.queue import notification_queue, priority_map, counter

router = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------- USER PREFERENCES -------------------

@router.post("/users/{user_id}/preferences")
def set_preferences(user_id: str, request: UserPreferenceCreate, db: Session = Depends(get_db)):
    pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()

    if pref:
        pref.email_enabled = request.email_enabled
        pref.sms_enabled = request.sms_enabled
        pref.push_enabled = request.push_enabled
    else:
        pref = UserPreference(
            user_id=user_id,
            email_enabled=request.email_enabled,
            sms_enabled=request.sms_enabled,
            push_enabled=request.push_enabled
        )
        db.add(pref)

    db.commit()
    return {"message": "Preferences updated"}


@router.get("/users/{user_id}/preferences")
def get_preferences(user_id: str, db: Session = Depends(get_db)):
    pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()

    if not pref:
        return {"message": "No preferences found"}

    return pref


# ------------------- NOTIFICATIONS -------------------

@router.post("/notifications")
def create_notification(request: NotificationCreate, db: Session = Depends(get_db)):
    new_notification = Notification(
        user_id=request.user_id,
        message=request.message,
        priority=request.priority,
        status="pending"
    )

    # Save to DB
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    # Push to queue
    priority = priority_map.get(request.priority, 3)

    notification_queue.put((
        priority,
        next(counter),  # 👈 tie-breaker
        {
            "id": new_notification.id,
            "user_id": new_notification.user_id,
            "message": new_notification.message
        }
    ))

    return {"message": "Notification created", "id": new_notification.id}


@router.get("/notifications/{notification_id}")
def get_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()

    if not notification:
        return {"error": "Notification not found"}

    return notification


@router.get("/users/{user_id}/notifications")
def get_user_notifications(user_id: str, db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.user_id == user_id).all()

    return notifications