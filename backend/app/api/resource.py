from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.resource import ResourceCreate, ResourceResponse, AllocationCreate, AllocationResponse
from app.services.resource_service import create_resource, allocate_resource, get_resources_by_project

router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("", response_model=ResourceResponse, status_code=201)
async def create_resource_endpoint(
    resource_data: ResourceCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new resource."""
    try:
        resource = await create_resource(db, resource_data)
        return resource
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/allocate", response_model=AllocationResponse, status_code=201)
async def allocate_resource_endpoint(
    allocation_data: AllocationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Allocate a resource to a project."""
    try:
        allocation = await allocate_resource(db, allocation_data)
        return allocation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}", response_model=List[ResourceResponse])
async def get_resources(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all resources for a project."""
    resources = await get_resources_by_project(db, project_id)
    return resources

