from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.models.risk import Risk
from app.schemas.risk import RiskAnalyze
from app.ai.llm_client import call_llm
from app.utils.file_utils import load_prompt
from app.services.risk_analytics_service import calculate_risk_score, record_risk_metric


def calculate_severity(probability: int, impact: int) -> str:
    """Calculate severity based on probability and impact."""
    score = probability * impact
    if score <= 6:
        return "low"
    elif score <= 15:
        return "medium"
    else:
        return "high"


async def analyze_risks_from_text(
    db: AsyncSession,
    risk_data: RiskAnalyze
) -> List[Risk]:
    """Analyze project text for risks using LLM."""
    prompt_template = load_prompt("risk_prompt")
    prompt = prompt_template.format(project_text=risk_data.project_text)
    
    system_prompt = "You are a risk management expert. Always return valid JSON."
    
    llm_response = await call_llm(prompt, system_prompt=system_prompt)
    
    risks_data = llm_response.get("risks", [])
    created_risks = []
    
    for risk_data_item in risks_data:
        category_str = risk_data_item.get("category", "external").lower()
        # Validate category is one of the allowed values
        valid_categories = ["schedule", "budget", "resource", "technical", "external"]
        category = category_str if category_str in valid_categories else "external"
        
        probability = int(risk_data_item.get("probability", 3))
        impact = int(risk_data_item.get("impact", 3))
        severity = risk_data_item.get("severity") or calculate_severity(probability, impact)
        risk_score = calculate_risk_score(probability, impact)
        
        risk = Risk(
            project_id=risk_data.project_id,
            title=risk_data_item.get("title", "Unnamed Risk"),
            description=risk_data_item.get("description", ""),
            category=category,
            probability=probability,
            impact=impact,
            severity=severity,
            risk_score=risk_score,
            trend="stable",
            mitigation_plan=risk_data_item.get("mitigation_plan"),
            status="open",
            approval_status="pending",
        )
        
        db.add(risk)
        created_risks.append(risk)
    
    await db.commit()
    
    for risk in created_risks:
        await db.refresh(risk)
        # Record initial metric
        await record_risk_metric(db, risk.id, risk.probability, risk.impact, risk.severity)
    
    return created_risks


async def analyze_project_documentation(
    db: AsyncSession,
    project_id: int
) -> List[Risk]:
    """Automatically analyze all project documentation for risks."""
    try:
        from app.models.project import Project
        from app.models.status_report import StatusReport
        from app.models.resource import Resource
        from app.models.allocation import Allocation
        
        # Verify project exists
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        
        # Gather project documentation
        status_result = await db.execute(
            select(StatusReport)
            .where(StatusReport.project_id == project_id)
            .order_by(StatusReport.report_date.desc())
        )
        status_reports = list(status_result.scalars().all())
        
        resource_result = await db.execute(
            select(Resource).where(Resource.project_id == project_id)
        )
        resources = list(resource_result.scalars().all())
        
        allocation_result = await db.execute(
            select(Allocation).where(Allocation.project_id == project_id)
        )
        allocations = list(allocation_result.scalars().all())
        
        # Check if there's any data to analyze
        if not status_reports and not resources and not allocations:
            raise ValueError(
            f"No data available to analyze for project '{project.name}'. "
            "Please add status reports, team members, or resource allocations before using AI analysis."
        doc_parts = [
            f"PROJECT OVERVIEW:",
            f"Name: {project.name}",
            f"Description: {project.description or 'N/A'}",
            f"Status: {project.status}",
            f"\n--- STATUS REPORTS ---"
        ]
        
        if status_reports:
            for sr in status_reports[:5]:  # Last 5 reports
                doc_parts.append(f"\nReport Date: {sr.report_date}")
                doc_parts.append(f"Progress: {sr.progress_summary}")
                doc_parts.append(f"Key Achievements: {sr.key_achievements or 'N/A'}")
                doc_parts.append(f"Upcoming Milestones: {sr.upcoming_milestones or 'N/A'}")
                doc_parts.append(f"Blockers: {sr.blockers or 'None'}")
        else:
            doc_parts.append("No status reports available.")
        
        doc_parts.append("\n--- RESOURCE ALLOCATIONS ---")
        if allocations:
            for alloc in allocations:
                # Find resource name
                resource = next((r for r in resources if r.id == alloc.resource_id), None)
                resource_name = resource.name if resource else "Unknown"
                doc_parts.append(
                    f"Resource: {resource_name}, "
                    f"Allocated Hours: {alloc.allocated_hours}h, "
                    f"Period: {alloc.start_date} to {alloc.end_date}"
                )
        else:
            doc_parts.append("No resource allocations available.")
        
        project_text = "\n".join(doc_parts)
        
        print(f"Analyzing project {project_id} with {len(status_reports)} reports, {len(resources)} resources")
        
        # Analyze with LLM
        prompt_template = load_prompt("risk_prompt")
        prompt = prompt_template.format(project_text=project_text)
        
        system_prompt = "You are a risk management expert analyzing comprehensive project documentation. Always return valid JSON."
        
        llm_response = await call_llm(prompt, system_prompt=system_prompt)
        
        risks_data = llm_response.get("risks", [])
        
        if not risks_data:
            print("Warning: LLM returned no risks")
            return []
        
        created_risks = []
        
        for risk_data_item in risks_data:
            category_str = risk_data_item.get("category", "external").lower()
            valid_categories = ["schedule", "budget", "resource", "technical", "external"]
            category = category_str if category_str in valid_categories else "external"
            
            probability = int(risk_data_item.get("probability", 3))
            impact = int(risk_data_item.get("impact", 3))
            severity = risk_data_item.get("severity") or calculate_severity(probability, impact)
            risk_score = calculate_risk_score(probability, impact)
            
            risk = Risk(
                project_id=project_id,
                title=risk_data_item.get("title", "Unnamed Risk"),
                description=risk_data_item.get("description", ""),
                category=category,
                probability=probability,
                impact=impact,
                severity=severity,
                risk_score=risk_score,
                trend="stable",
                mitigation_plan=risk_data_item.get("mitigation_plan"),
                status="open",
                approval_status="pending",
            )
            
            db.add(risk)
            created_risks.append(risk)
        
        await db.commit()
        
        # Refresh to get IDs
        for risk in created_risks:
            await db.refresh(risk)
            # Record initial metric
            await record_risk_metric(db, risk.id, risk.probability, risk.impact, risk.severity)
        
        await db.commit()
        
        print(f"Successfully created {len(created_risks)} risks for project {project_id}")
        return created_risks
        
    except ValueError:
        # Re-raise validation errors as-is
        raise
    except Exception as e:
        import traceback
        print(f"Error in analyze_project_documentation: {str(e)}")
        print(traceback.format_exc())
        raise
    db: AsyncSession,
    project_id: int
) -> List[Risk]:
    """Automatically analyze all project documentation for risks."""
    from app.models.project import Project
    from app.models.status_report import StatusReport
    from app.models.resource import Resource
    from app.models.allocation import Allocation
    
    # Fetch project details
    project_result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = project_result.scalar_one_or_none()
    if not project:
        raise ValueError(f"Project {project_id} not found")
    
    # Fetch status reports
    status_result = await db.execute(
        select(StatusReport)
        .where(StatusReport.project_id == project_id)
        .order_by(StatusReport.created_at.desc())
    )
    status_reports = list(status_result.scalars().all())
    
    # Fetch resources
    resource_result = await db.execute(select(Resource))
    resources = list(resource_result.scalars().all())
    
    # Fetch allocations for this project
    allocation_result = await db.execute(
        select(Allocation).where(Allocation.project_id == project_id)
    )
    allocations = list(allocation_result.scalars().all())
    
    # Compile documentation
    doc_parts = [
        f"PROJECT OVERVIEW:",
        f"Name: {project.name}",
        f"Description: {project.description or 'N/A'}",
        f"Status: {project.status}",
        f"\n--- STATUS REPORTS ---"
    ]
    
    for sr in status_reports[:5]:  # Last 5 reports
        doc_parts.append(f"\nReport Date: {sr.report_date}")
        doc_parts.append(f"Progress: {sr.progress_summary}")
        doc_parts.append(f"Key Achievements: {sr.key_achievements or 'N/A'}")
        doc_parts.append(f"Upcoming Milestones: {sr.upcoming_milestones or 'N/A'}")
        doc_parts.append(f"Blockers: {sr.blockers or 'None'}")
    
    doc_parts.append("\n--- RESOURCE ALLOCATIONS ---")
    for alloc in allocations:
        # Find resource name
        resource = next((r for r in resources if r.id == alloc.resource_id), None)
        resource_name = resource.name if resource else "Unknown"
        doc_parts.append(
            f"Resource: {resource_name}, "
            f"Allocated Hours: {alloc.allocated_hours}h, "
            f"Period: {alloc.start_date} to {alloc.end_date}"
        )
    
    project_text = "\n".join(doc_parts)
    
    # Analyze with LLM
    prompt_template = load_prompt("risk_prompt")
    prompt = prompt_template.format(project_text=project_text)
    
    system_prompt = "You are a risk management expert analyzing comprehensive project documentation. Always return valid JSON."
    
    llm_response = await call_llm(prompt, system_prompt=system_prompt)
    
    risks_data = llm_response.get("risks", [])
    created_risks = []
    
    for risk_data_item in risks_data:
        category_str = risk_data_item.get("category", "external").lower()
        valid_categories = ["schedule", "budget", "resource", "technical", "external"]
        category = category_str if category_str in valid_categories else "external"
        
        probability = int(risk_data_item.get("probability", 3))
        impact = int(risk_data_item.get("impact", 3))
        severity = risk_data_item.get("severity") or calculate_severity(probability, impact)
        risk_score = calculate_risk_score(probability, impact)
        
        risk = Risk(
            project_id=project_id,
            title=risk_data_item.get("title", "Unnamed Risk"),
            description=risk_data_item.get("description", ""),
            category=category,
            probability=probability,
            impact=impact,
            severity=severity,
            risk_score=risk_score,
            trend="stable",
            mitigation_plan=risk_data_item.get("mitigation_plan"),
            status="open",
            approval_status="pending",
        )
        
        db.add(risk)
        created_risks.append(risk)
    
    await db.commit()
    
    for risk in created_risks:
        await db.refresh(risk)
        await record_risk_metric(db, risk.id, risk.probability, risk.impact, risk.severity)
    
    return created_risks


async def get_risks_by_project(
    db: AsyncSession,
    project_id: int
) -> List[Risk]:
    """Get all risks for a project."""
    result = await db.execute(
        select(Risk)
        .where(Risk.project_id == project_id)
        .order_by(Risk.created_at.desc())
    )
    return list(result.scalars().all())
