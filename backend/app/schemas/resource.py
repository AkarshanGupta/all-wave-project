from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal


class ResourceSkillCreate(BaseModel):
    skill_name: str
    proficiency_level: int  # 1-5


class ResourceSkillResponse(BaseModel):
    id: int
    resource_id: int
    skill_name: str
    proficiency_level: int

    class Config:
        from_attributes = True


class ResourceCreate(BaseModel):
    project_id: Optional[int] = None
    name: str
    role: str
    capacity_hours: Decimal
    availability_hours: Decimal
    department: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[List[ResourceSkillCreate]] = []


class AllocationCreate(BaseModel):
    resource_id: int
    project_id: int
    allocated_hours: Decimal
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class AllocationResponse(BaseModel):
    id: int
    resource_id: int
    project_id: int
    allocated_hours: Decimal
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ResourceResponse(BaseModel):
    id: int
    project_id: Optional[int]
    name: str
    role: str
    capacity_hours: Decimal
    availability_hours: Decimal
    department: Optional[str]
    location: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    allocations: List[AllocationResponse] = []
    skills: List[ResourceSkillResponse] = []

    class Config:
        from_attributes = True


class ProjectRequirementCreate(BaseModel):
    project_id: int
    skill_name: str
    required_proficiency: int  # 1-5
    required_hours: Decimal
    description: Optional[str] = None


class ProjectRequirementResponse(BaseModel):
    id: int
    project_id: int
    skill_name: str
    required_proficiency: int
    required_hours: Decimal
    description: Optional[str]

    class Config:
        from_attributes = True


class ResourceUtilizationResponse(BaseModel):
    resource_id: int
    resource_name: str
    capacity_hours: Decimal
    allocated_hours: Decimal
    available_hours: Decimal
    utilization_percentage: float
    status: str  # "under-utilized", "optimal", "over-utilized"
    allocations: List[Dict[str, Any]]


class SchedulingConflict(BaseModel):
    resource_id: int
    resource_name: str
    conflict_type: str
    description: str
    affected_projects: List[int]
    severity: str  # "low", "medium", "high"
    suggested_resolution: Optional[str]


class ResourceRecommendation(BaseModel):
    resource_id: int
    resource_name: str
    project_id: int
    project_name: str
    match_score: float  # 0-100
    skill_match: Dict[str, Any]
    availability_score: float
    reasoning: str


class AllocationOptimizationResponse(BaseModel):
    recommendations: List[ResourceRecommendation]
    conflicts: List[SchedulingConflict]
    utilization_summary: Dict[str, Any]
    optimization_score: float


class ScenarioCreate(BaseModel):
    name: str
    description: Optional[str] = None
    allocations: List[AllocationCreate]


class ScenarioResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    scenario_data: Dict[str, Any]
    metrics: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ScenarioComparisonResponse(BaseModel):
    scenarios: List[ScenarioResponse]
    comparison_metrics: Dict[str, Any]
    recommendations: str


