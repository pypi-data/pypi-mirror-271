from pydantic import BaseModel,EmailStr
from datetime import datetime

class Message(BaseModel):
    id: int
    sender: str
    recipient: str
    content: str
class MailerDto(BaseModel):
    recipients: list[EmailStr]
    subject: str
    message: str
    create_at: datetime
    is_html: bool