from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal


class ResourceCreate(BaseModel):
    project_id: Optional[int] = None
    name: str
    role: str
    capacity_hours: Decimal
    availability_hours: Decimal


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
    created_at: datetime
    updated_at: Optional[datetime]
    allocations: list[AllocationResponse] = []

    class Config:
        from_attributes = True

