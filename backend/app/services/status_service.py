from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from app.models.status_report import StatusReport
from app.models.project import Project
from app.models.risk import Risk
from app.models.meeting import Meeting
from app.models.resource import Resource, Allocation
from app.ai.llm_client import call_llm
from app.utils.file_utils import load_prompt
import json


async def generate_status_report(
    db: AsyncSession,
    project_id: int
) -> StatusReport:
    """Generate status report by aggregating project data and using LLM."""
    project_result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = project_result.scalar_one_or_none()
    
    if not project:
        raise ValueError(f"Project {project_id} not found")
    
    risks_result = await db.execute(
        select(Risk).where(Risk.project_id == project_id)
    )
    risks = risks_result.scalars().all()
    
    meetings_result = await db.execute(
        select(Meeting).where(Meeting.project_id == project_id)
        .order_by(Meeting.created_at.desc())
        .limit(5)
    )
    meetings = meetings_result.scalars().all()
    
    resources_result = await db.execute(
        select(Resource).where(Resource.project_id == project_id)
    )
    resources = resources_result.scalars().all()
    
    allocations_result = await db.execute(
        select(Allocation).where(Allocation.project_id == project_id)
    )
    allocations = allocations_result.scalars().all()
    
    total_allocated = sum(float(alloc.allocated_hours) for alloc in allocations)
    
    project_info = {
        "project_name": project.name,
        "project_description": project.description or "",
        "project_status": project.status,
        "risks": [
            {
                "title": risk.title,
                "category": risk.category.value,
                "severity": risk.severity,
                "status": risk.status,
            }
            for risk in risks
        ],
        "recent_meetings": [
            {
                "title": meeting.title,
                "summary": meeting.summary or "",
                "decisions": meeting.decisions or "",
            }
            for meeting in meetings
        ],
        "resources": [
            {
                "name": resource.name,
                "role": resource.role,
                "capacity_hours": float(resource.capacity_hours),
                "availability_hours": float(resource.availability_hours),
            }
            for resource in resources
        ],
        "total_allocated_hours": total_allocated,
    }
    
    prompt_template = load_prompt("status_prompt")
    prompt = prompt_template.format(project_info=json.dumps(project_info, indent=2))
    
    system_prompt = "You are an executive assistant. Always return valid JSON."
    
    llm_response = await call_llm(prompt, system_prompt=system_prompt)
    
    risks_summary = f"Total risks: {len(risks)}. "
    if risks:
        high_risks = [r for r in risks if r.severity == "high"]
        risks_summary += f"High severity: {len(high_risks)}. "
    
    meetings_summary = f"Total meetings: {len(meetings)}"
    if meetings:
        latest = meetings[0]
        meetings_summary += f". Latest: {latest.title}"
    
    resources_summary = f"Resources: {len(resources)}, Total allocated hours: {total_allocated}"
    
    status_report = StatusReport(
        project_id=project_id,
        executive_summary=llm_response.get("executive_summary", ""),
        risks_summary=risks_summary,
        meetings_summary=meetings_summary,
        resources_summary=resources_summary,
    )
    
    db.add(status_report)
    await db.commit()
    await db.refresh(status_report)
    
    return status_report


async def get_status_report_by_project(
    db: AsyncSession,
    project_id: int
) -> StatusReport:
    """Get the latest status report for a project."""
    result = await db.execute(
        select(StatusReport)
        .where(StatusReport.project_id == project_id)
        .order_by(StatusReport.generated_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()

