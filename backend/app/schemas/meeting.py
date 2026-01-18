from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ActionItemCreate(BaseModel):
    description: str
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    status: str = "open"


class ActionItemResponse(BaseModel):
    id: int
    meeting_id: int
    description: str
    assignee: Optional[str]
    due_date: Optional[datetime]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class MeetingUpload(BaseModel):
    project_id: int
    title: str
    raw_text: str


class MeetingCreate(BaseModel):
    project_id: int
    title: str
    raw_text: str
    summary: Optional[str] = None


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None


class MeetingResponse(BaseModel):
    id: int
    project_id: int
    title: str
    raw_text: str
    summary: Optional[str]
    decisions: Optional[str]
    open_questions: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


