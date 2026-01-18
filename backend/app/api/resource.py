from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.schemas.resource import (
    ResourceCreate, 
    ResourceResponse, 
    AllocationCreate, 
    AllocationResponse,
    ResourceSkillCreate,
    ResourceSkillResponse,
    ProjectRequirementCreate,
    ProjectRequirementResponse,
    ResourceUtilizationResponse,
    SchedulingConflict,
    AllocationOptimizationResponse,
    ScenarioCreate,
    ScenarioResponse,
    ScenarioComparisonResponse
)
from app.services.resource_service import create_resource, allocate_resource, get_resources_by_project
from app.services.allocation_optimizer_service import (
    get_resource_utilization,
    detect_scheduling_conflicts,
    recommend_optimal_allocation,
    create_allocation_scenario,
    compare_scenarios
)

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=List[ResourceResponse])
async def get_all_resources(
    db: AsyncSession = Depends(get_db)
):
    """Get all resources."""
    from app.models.resource import Resource
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    
    result = await db.execute(
        select(Resource)
        .options(selectinload(Resource.allocations))
        .options(selectinload(Resource.skills))
    )
    resources = result.scalars().all()
    return resources


@router.post("", response_model=ResourceResponse, status_code=201)
async def create_resource_endpoint(
    resource_data: ResourceCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new resource with optional skills."""
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


# ============ Module 3: Resource Allocation Optimizer Endpoints ============

@router.get("/utilization/all", response_model=List[ResourceUtilizationResponse])
async def get_all_resource_utilization(
    db: AsyncSession = Depends(get_db)
):
    """
    Get utilization metrics for all resources.
    Identifies over-utilized and under-utilized resources.
    """
    try:
        return await get_resource_utilization(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/utilization/{resource_id}", response_model=List[ResourceUtilizationResponse])
async def get_single_resource_utilization(
    resource_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get utilization metrics for a specific resource."""
    try:
        return await get_resource_utilization(db, resource_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conflicts/detect", response_model=List[SchedulingConflict])
async def detect_conflicts(
    project_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Detect scheduling conflicts including over-allocation and date overlaps.
    Optionally filter by project_id.
    """
    try:
        return await detect_scheduling_conflicts(db, project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize/{project_id}", response_model=AllocationOptimizationResponse)
async def optimize_allocation(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Recommend optimal resource allocation for a project.
    Considers skill matching, availability, and development opportunities.
    """
    try:
        return await recommend_optimal_allocation(db, project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scenarios", response_model=ScenarioResponse, status_code=201)
async def create_scenario(
    scenario_data: ScenarioCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a what-if scenario for resource allocation analysis.
    Test different allocation strategies without affecting actual data.
    """
    try:
        return await create_allocation_scenario(db, scenario_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scenarios/compare", response_model=ScenarioComparisonResponse)
async def compare_allocation_scenarios(
    scenario_ids: List[int],
    db: AsyncSession = Depends(get_db)
):
    """
    Compare multiple allocation scenarios and get recommendations.
    Helps choose the best allocation strategy.
    """
    try:
        return await compare_scenarios(db, scenario_ids)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/skills/{resource_id}", response_model=ResourceSkillResponse, status_code=201)
async def add_resource_skill(
    resource_id: int,
    skill_data: ResourceSkillCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add a skill to a resource profile."""
    from app.models.resource_skill import ResourceSkill
    from app.models.resource import Resource
    from sqlalchemy import select
    
    try:
        # Verify resource exists
        result = await db.execute(select(Resource).where(Resource.id == resource_id))
        resource = result.scalar_one_or_none()
        if not resource:
            raise HTTPException(status_code=404, detail=f"Resource {resource_id} not found")
        
        skill = ResourceSkill(
            resource_id=resource_id,
            skill_name=skill_data.skill_name,
            proficiency_level=skill_data.proficiency_level
        )
        db.add(skill)
        await db.commit()
        await db.refresh(skill)
        return skill
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/requirements/{project_id}", response_model=ProjectRequirementResponse, status_code=201)
async def add_project_requirement(
    project_id: int,
    requirement_data: ProjectRequirementCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add a skill requirement to a project."""
    from app.models.project_requirement import ProjectRequirement
    from app.models.project import Project
    from sqlalchemy import select
    
    try:
        # Verify project exists
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        
        requirement = ProjectRequirement(
            project_id=project_id,
            skill_name=requirement_data.skill_name,
            required_proficiency=requirement_data.required_proficiency,
            required_hours=requirement_data.required_hours,
            description=requirement_data.description
        )
        db.add(requirement)
        await db.commit()
        await db.refresh(requirement)
        return requirement
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

