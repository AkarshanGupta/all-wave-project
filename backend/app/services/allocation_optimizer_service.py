"""
Resource Allocation Optimizer Service
Provides intelligent resource allocation, conflict detection, utilization analysis, and scenario planning.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Dict, Any, Tuple
from decimal import Decimal
from datetime import datetime, timedelta
from app.models.resource import Resource, Allocation
from app.models.resource_skill import ResourceSkill
from app.models.project_requirement import ProjectRequirement
from app.models.allocation_scenario import AllocationScenario
from app.models.project import Project
from app.schemas.resource import (
    ResourceUtilizationResponse,
    SchedulingConflict,
    ResourceRecommendation,
    AllocationOptimizationResponse,
    ScenarioCreate,
    ScenarioResponse,
    ScenarioComparisonResponse
)


async def get_resource_utilization(
    db: AsyncSession,
    resource_id: Optional[int] = None
) -> List[ResourceUtilizationResponse]:
    """
    Calculate utilization for all resources or a specific resource.
    Identifies over-utilized and under-utilized resources.
    """
    if resource_id:
        resource_result = await db.execute(
            select(Resource).where(Resource.id == resource_id)
        )
        resources = [resource_result.scalar_one_or_none()]
        if not resources[0]:
            return []
    else:
        resource_result = await db.execute(select(Resource))
        resources = list(resource_result.scalars().all())
    
    utilization_data = []
    
    for resource in resources:
        # Calculate total allocated hours
        allocation_result = await db.execute(
            select(func.sum(Allocation.allocated_hours))
            .where(Allocation.resource_id == resource.id)
        )
        total_allocated = allocation_result.scalar() or Decimal("0")
        
        # Get all allocations
        allocations_result = await db.execute(
            select(Allocation).where(Allocation.resource_id == resource.id)
        )
        allocations = list(allocations_result.scalars().all())
        
        # Calculate available hours
        available_hours = resource.capacity_hours - total_allocated
        
        # Calculate utilization percentage
        utilization_pct = float((total_allocated / resource.capacity_hours) * 100) if resource.capacity_hours > 0 else 0
        
        # Determine status
        if utilization_pct < 60:
            status = "under-utilized"
        elif utilization_pct <= 90:
            status = "optimal"
        else:
            status = "over-utilized"
        
        # Prepare allocation details
        allocation_details = []
        for alloc in allocations:
            project_result = await db.execute(
                select(Project).where(Project.id == alloc.project_id)
            )
            project = project_result.scalar_one_or_none()
            
            allocation_details.append({
                "project_id": alloc.project_id,
                "project_name": project.name if project else "Unknown",
                "allocated_hours": float(alloc.allocated_hours),
                "start_date": alloc.start_date.isoformat() if alloc.start_date else None,
                "end_date": alloc.end_date.isoformat() if alloc.end_date else None,
            })
        
        utilization_data.append(ResourceUtilizationResponse(
            resource_id=resource.id,
            resource_name=resource.name,
            capacity_hours=resource.capacity_hours,
            allocated_hours=total_allocated,
            available_hours=available_hours,
            utilization_percentage=round(utilization_pct, 2),
            status=status,
            allocations=allocation_details
        ))
    
    return utilization_data


async def detect_scheduling_conflicts(
    db: AsyncSession,
    project_id: Optional[int] = None
) -> List[SchedulingConflict]:
    """
    Detect scheduling conflicts including:
    - Over-allocation (resource capacity exceeded)
    - Date overlaps (same resource on multiple projects in same timeframe)
    - Skill mismatches
    """
    conflicts = []
    
    # Get all resources
    resource_result = await db.execute(select(Resource))
    resources = list(resource_result.scalars().all())
    
    for resource in resources:
        # Check over-allocation
        allocation_result = await db.execute(
            select(func.sum(Allocation.allocated_hours))
            .where(Allocation.resource_id == resource.id)
        )
        total_allocated = allocation_result.scalar() or Decimal("0")
        
        if total_allocated > resource.capacity_hours:
            allocations_result = await db.execute(
                select(Allocation).where(Allocation.resource_id == resource.id)
            )
            allocations = list(allocations_result.scalars().all())
            affected_projects = [alloc.project_id for alloc in allocations]
            
            over_allocated_hours = float(total_allocated - resource.capacity_hours)
            
            conflicts.append(SchedulingConflict(
                resource_id=resource.id,
                resource_name=resource.name,
                conflict_type="over-allocation",
                description=f"Resource is over-allocated by {over_allocated_hours} hours",
                affected_projects=affected_projects,
                severity="high",
                suggested_resolution=f"Reduce allocation or increase capacity by {over_allocated_hours} hours"
            ))
        
        # Check date overlaps
        allocations_result = await db.execute(
            select(Allocation)
            .where(
                and_(
                    Allocation.resource_id == resource.id,
                    Allocation.start_date.isnot(None),
                    Allocation.end_date.isnot(None)
                )
            )
            .order_by(Allocation.start_date)
        )
        allocations = list(allocations_result.scalars().all())
        
        for i in range(len(allocations)):
            for j in range(i + 1, len(allocations)):
                alloc1, alloc2 = allocations[i], allocations[j]
                
                # Check if date ranges overlap
                if alloc1.end_date >= alloc2.start_date and alloc2.end_date >= alloc1.start_date:
                    conflicts.append(SchedulingConflict(
                        resource_id=resource.id,
                        resource_name=resource.name,
                        conflict_type="date-overlap",
                        description=f"Overlapping allocations from {alloc1.start_date.date()} to {alloc2.end_date.date()}",
                        affected_projects=[alloc1.project_id, alloc2.project_id],
                        severity="medium",
                        suggested_resolution="Adjust project timelines or assign additional resources"
                    ))
    
    return conflicts


async def calculate_skill_match_score(
    db: AsyncSession,
    resource_id: int,
    project_id: int
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculate how well a resource's skills match project requirements.
    Returns match score (0-100) and detailed skill comparison.
    """
    # Get resource skills
    skills_result = await db.execute(
        select(ResourceSkill).where(ResourceSkill.resource_id == resource_id)
    )
    resource_skills = {skill.skill_name: skill.proficiency_level for skill in skills_result.scalars().all()}
    
    # Get project requirements
    requirements_result = await db.execute(
        select(ProjectRequirement).where(ProjectRequirement.project_id == project_id)
    )
    requirements = list(requirements_result.scalars().all())
    
    if not requirements:
        return 50.0, {"message": "No specific requirements defined"}
    
    total_score = 0
    max_score = 0
    skill_details = {}
    
    for req in requirements:
        max_score += 100
        resource_proficiency = resource_skills.get(req.skill_name, 0)
        
        if resource_proficiency >= req.required_proficiency:
            # Perfect match or better
            score = 100
        elif resource_proficiency > 0:
            # Partial match
            score = (resource_proficiency / req.required_proficiency) * 80
        else:
            # No match
            score = 0
        
        total_score += score
        
        skill_details[req.skill_name] = {
            "required": req.required_proficiency,
            "actual": resource_proficiency,
            "match": "excellent" if score == 100 else "partial" if score > 0 else "none",
            "score": round(score, 2)
        }
    
    overall_score = (total_score / max_score * 100) if max_score > 0 else 0
    
    return round(overall_score, 2), skill_details


async def recommend_optimal_allocation(
    db: AsyncSession,
    project_id: int
) -> AllocationOptimizationResponse:
    """
    Recommend optimal resource allocation for a project based on:
    - Skill matching
    - Availability
    - Current utilization
    - Development opportunities
    """
    # Get project details
    project_result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = project_result.scalar_one_or_none()
    
    if not project:
        raise ValueError(f"Project {project_id} not found")
    
    # Get all available resources
    resources_result = await db.execute(select(Resource))
    resources = list(resources_result.scalars().all())
    
    recommendations = []
    
    for resource in resources:
        # Calculate skill match
        skill_score, skill_match = await calculate_skill_match_score(db, resource.id, project_id)
        
        # Calculate availability
        allocation_result = await db.execute(
            select(func.sum(Allocation.allocated_hours))
            .where(Allocation.resource_id == resource.id)
        )
        total_allocated = allocation_result.scalar() or Decimal("0")
        available_hours = resource.capacity_hours - total_allocated
        availability_score = min(100, float(available_hours / resource.capacity_hours * 100))
        
        # Calculate overall match score (weighted average)
        match_score = (skill_score * 0.7) + (availability_score * 0.3)
        
        # Generate reasoning
        reasoning_parts = []
        if skill_score >= 80:
            reasoning_parts.append("Excellent skill match")
        elif skill_score >= 60:
            reasoning_parts.append("Good skill match with development opportunity")
        else:
            reasoning_parts.append("Skills need development")
        
        if availability_score >= 50:
            reasoning_parts.append(f"{float(available_hours)}h available")
        else:
            reasoning_parts.append("Limited availability")
        
        if match_score >= 60:  # Only recommend if reasonable match
            recommendations.append(ResourceRecommendation(
                resource_id=resource.id,
                resource_name=resource.name,
                project_id=project_id,
                project_name=project.name,
                match_score=round(match_score, 2),
                skill_match=skill_match,
                availability_score=round(availability_score, 2),
                reasoning="; ".join(reasoning_parts)
            ))
    
    # Sort by match score
    recommendations.sort(key=lambda x: x.match_score, reverse=True)
    
    # Get conflicts
    conflicts = await detect_scheduling_conflicts(db, project_id)
    
    # Get utilization summary
    utilization = await get_resource_utilization(db)
    utilization_summary = {
        "total_resources": len(utilization),
        "under_utilized": len([u for u in utilization if u.status == "under-utilized"]),
        "optimal": len([u for u in utilization if u.status == "optimal"]),
        "over_utilized": len([u for u in utilization if u.status == "over-utilized"]),
        "avg_utilization": round(sum([u.utilization_percentage for u in utilization]) / len(utilization), 2) if utilization else 0
    }
    
    # Calculate optimization score
    optimization_score = 100
    if conflicts:
        optimization_score -= len(conflicts) * 10
    if utilization_summary["over_utilized"] > 0:
        optimization_score -= utilization_summary["over_utilized"] * 15
    optimization_score = max(0, optimization_score)
    
    return AllocationOptimizationResponse(
        recommendations=recommendations[:10],  # Top 10
        conflicts=conflicts,
        utilization_summary=utilization_summary,
        optimization_score=optimization_score
    )


async def create_allocation_scenario(
    db: AsyncSession,
    scenario_data: ScenarioCreate
) -> ScenarioResponse:
    """
    Create a what-if scenario for resource allocation analysis.
    """
    # Calculate metrics for this scenario
    total_hours = sum([alloc.allocated_hours for alloc in scenario_data.allocations])
    unique_resources = len(set([alloc.resource_id for alloc in scenario_data.allocations]))
    unique_projects = len(set([alloc.project_id for alloc in scenario_data.allocations]))
    
    metrics = {
        "total_allocated_hours": float(total_hours),
        "resources_involved": unique_resources,
        "projects_involved": unique_projects,
        "allocations_count": len(scenario_data.allocations)
    }
    
    # Convert allocations to JSON-serializable format
    scenario_json = {
        "allocations": [
            {
                "resource_id": alloc.resource_id,
                "project_id": alloc.project_id,
                "allocated_hours": float(alloc.allocated_hours),
                "start_date": alloc.start_date.isoformat() if alloc.start_date else None,
                "end_date": alloc.end_date.isoformat() if alloc.end_date else None
            }
            for alloc in scenario_data.allocations
        ]
    }
    
    scenario = AllocationScenario(
        name=scenario_data.name,
        description=scenario_data.description,
        scenario_data=scenario_json,
        metrics=metrics
    )
    
    db.add(scenario)
    await db.commit()
    await db.refresh(scenario)
    
    return ScenarioResponse.from_orm(scenario)


async def compare_scenarios(
    db: AsyncSession,
    scenario_ids: List[int]
) -> ScenarioComparisonResponse:
    """
    Compare multiple allocation scenarios and provide recommendations.
    """
    scenarios = []
    
    for scenario_id in scenario_ids:
        result = await db.execute(
            select(AllocationScenario).where(AllocationScenario.id == scenario_id)
        )
        scenario = result.scalar_one_or_none()
        if scenario:
            scenarios.append(ScenarioResponse.from_orm(scenario))
    
    if not scenarios:
        raise ValueError("No valid scenarios found")
    
    # Compare metrics
    comparison_metrics = {
        "total_hours": [s.metrics.get("total_allocated_hours", 0) for s in scenarios],
        "resources_used": [s.metrics.get("resources_involved", 0) for s in scenarios],
        "projects_covered": [s.metrics.get("projects_involved", 0) for s in scenarios],
        "allocations_count": [s.metrics.get("allocations_count", 0) for s in scenarios]
    }
    
    # Generate recommendations
    best_scenario_idx = comparison_metrics["total_hours"].index(min(comparison_metrics["total_hours"]))
    recommendations = f"Scenario '{scenarios[best_scenario_idx].name}' appears most efficient with {comparison_metrics['total_hours'][best_scenario_idx]} total hours allocated."
    
    return ScenarioComparisonResponse(
        scenarios=scenarios,
        comparison_metrics=comparison_metrics,
        recommendations=recommendations
    )


from typing import Optional
