from pydantic import BaseModel
from datetime import datetime


class StatusReportResponse(BaseModel):
    id: int
    project_id: int
    executive_summary: str
    risks_summary: str | None
    meetings_summary: str | None
    resources_summary: str | None
    generated_at: datetime

    class Config:
        from_attributes = True

