from pydantic import BaseModel # pyright: ignore[reportMissingImports]
from typing import List, Optional


class NotificationCreate(BaseModel):
    user_id: str
    message: str
    channels: List[str]   # ["email", "sms"]
    priority: str


class NotificationResponse(BaseModel):
    id: int
    user_id: str
    message: str
    priority: str
    status: str

    class Config:
     from_attributes = True