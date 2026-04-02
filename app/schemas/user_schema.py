from pydantic import BaseModel


class UserPreferenceCreate(BaseModel):
    email_enabled: bool = True
    sms_enabled: bool = True
    push_enabled: bool = True