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
