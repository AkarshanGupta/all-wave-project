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
    date: Optional[str] = None  # YYYY-MM-DD format
    time: Optional[str] = None  # HH:MM format
    duration: Optional[int] = None  # minutes
    attendees: Optional[List[str]] = None
    status: Optional[str] = "scheduled"


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    duration: Optional[int] = None
    attendees: Optional[List[str]] = None
    status: Optional[str] = None


class MeetingResponse(BaseModel):
    id: int
    project_id: int
    title: str
    raw_text: str
    summary: Optional[str]
    decisions: Optional[str]
    open_questions: Optional[str]
    date: Optional[str]
    time: Optional[str]
    duration: Optional[int]
    attendees: Optional[List[str]]
    status: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


