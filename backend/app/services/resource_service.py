from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from decimal import Decimal
from app.models.resource import Resource, Allocation
from app.models.resource_skill import ResourceSkill
from app.schemas.resource import ResourceCreate, AllocationCreate


async def create_resource(
    db: AsyncSession,
    resource_data: ResourceCreate
) -> Resource:
    """Create a new resource with optional skills."""
    resource = Resource(
        project_id=resource_data.project_id,
        name=resource_data.name,
        role=resource_data.role,
        capacity_hours=resource_data.capacity_hours,
        availability_hours=resource_data.availability_hours,
        department=resource_data.department,
        location=resource_data.location,
    )
    
    db.add(resource)
    await db.flush()  # Get resource ID
    
    # Add skills if provided
    if resource_data.skills:
        for skill_data in resource_data.skills:
            skill = ResourceSkill(
                resource_id=resource.id,
                skill_name=skill_data.skill_name,
                proficiency_level=skill_data.proficiency_level
            )
            db.add(skill)
    
    await db.commit()
    await db.refresh(resource)
    
    return resource


async def allocate_resource(
    db: AsyncSession,
    allocation_data: AllocationCreate
) -> Allocation:
    """Allocate a resource to a project with rule-based logic."""
    resource_result = await db.execute(
        select(Resource).where(Resource.id == allocation_data.resource_id)
    )
    resource = resource_result.scalar_one_or_none()
    
    if not resource:
        raise ValueError(f"Resource {allocation_data.resource_id} not found")
    
    existing_allocations_result = await db.execute(
        select(func.sum(Allocation.allocated_hours))
        .where(Allocation.resource_id == allocation_data.resource_id)
    )
    total_allocated = existing_allocations_result.scalar() or Decimal("0")
    
    new_total = total_allocated + allocation_data.allocated_hours
    
    if new_total > resource.capacity_hours:
        raise ValueError(
            f"Allocation exceeds capacity. "
            f"Current: {total_allocated}, Requested: {allocation_data.allocated_hours}, "
            f"Capacity: {resource.capacity_hours}"
        )
    
    allocation = Allocation(
        resource_id=allocation_data.resource_id,
        project_id=allocation_data.project_id,
        allocated_hours=allocation_data.allocated_hours,
        start_date=allocation_data.start_date,
        end_date=allocation_data.end_date,
    )
    
    db.add(allocation)
    await db.commit()
    await db.refresh(allocation)
    
    return allocation


async def get_resources_by_project(
    db: AsyncSession,
    project_id: int
) -> List[Resource]:
    """Get all resources for a project."""
    result = await db.execute(
        select(Resource)
        .where(Resource.project_id == project_id)
        .order_by(Resource.created_at.desc())
    )
    resources = result.scalars().all()
    
    for resource in resources:
        allocations_result = await db.execute(
            select(Allocation)
            .where(Allocation.resource_id == resource.id)
        )
        resource.allocations = list(allocations_result.scalars().all())
    
    return list(resources)

