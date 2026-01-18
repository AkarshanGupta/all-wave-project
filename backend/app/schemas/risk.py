from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


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
    approval_status: Optional[str] = None
    approved_by: Optional[str] = None


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
    risk_score: Optional[float] = 0.0
    trend: Optional[str] = "stable"
    mitigation_plan: Optional[str] = None
    status: Optional[str] = "open"
    approval_status: Optional[str] = "pending"
    approved_by: Optional[str] = None
    is_escalated: Optional[int] = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RiskAnalyticsResponse(BaseModel):
    total_risks: int
    high_severity_count: int
    escalated_count: int
    approval_pending: int
    average_risk_score: float
    risks_by_category: dict
    risks_by_severity: dict
    risks_by_status: dict


class RiskMatrixDataResponse(BaseModel):
    risks: List[RiskResponse]
    probability_range: tuple
    impact_range: tuple

