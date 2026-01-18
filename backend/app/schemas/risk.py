from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RiskCreate(BaseModel):
    project_id: int
    title: str
    description: str
    category: str
    probability: int
    impact: int
    severity: str
    mitigation_plan: Optional[str] = None
    status: Optional[str] = "open"


class RiskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    probability: Optional[int] = None
    impact: Optional[int] = None
    severity: Optional[str] = None
    mitigation_plan: Optional[str] = None
    status: Optional[str] = None


class RiskAnalyze(BaseModel):
    project_id: int
    project_text: str


class RiskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    category: str
    probability: int
    impact: int
    severity: str
    mitigation_plan: Optional[str]
    status: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


