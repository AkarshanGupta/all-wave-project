from pydantic import BaseModel, field_serializer, field_validator, model_serializer
from datetime import datetime, date
from typing import Optional, List, Any
import json


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
    
    @model_serializer
    def serialize_model(self) -> dict[str, Any]:
        """Custom serializer to handle date and attendees conversion."""
        data = {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'raw_text': self.raw_text,
            'summary': self.summary,
            'decisions': self.decisions,
            'open_questions': self.open_questions,
            'date': self.date.strftime("%Y-%m-%d") if isinstance(self.date, date) else self.date,
            'time': self.time,
            'duration': self.duration,
            'attendees': self.attendees if isinstance(self.attendees, list) else [],
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
        return data
    
    @field_validator('attendees', mode='before')
    @classmethod
    def parse_attendees(cls, value):
        """Parse attendees from JSON string if needed."""
        if value is None:
            return []
        if isinstance(value, str):
            try:
                return json.loads(value) if value else []
            except:
                return []
        return value if isinstance(value, list) else []


