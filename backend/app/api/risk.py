from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.risk import Risk
from app.schemas.risk import RiskAnalyze, RiskResponse, RiskCreate, RiskUpdate
from app.services.risk_service import analyze_risks_from_text, get_risks_by_project

router = APIRouter(prefix="/risks", tags=["risks"])


@router.post("/analyze", response_model=List[RiskResponse], status_code=201)
async def analyze_risks(
    risk_data: RiskAnalyze,
    db: AsyncSession = Depends(get_db)
):
    """Analyze project text for risks using LLM."""
    try:
        risks = await analyze_risks_from_text(db, risk_data)
        return risks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=RiskResponse, status_code=201)
async def create_risk(
    risk_data: RiskCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new risk."""
    # Verify project exists
    from app.models.project import Project
    result = await db.execute(select(Project).where(Project.id == risk_data.project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"Project with id {risk_data.project_id} not found. Please create the project first."
        )
    
    risk = Risk(
        project_id=risk_data.project_id,
        title=risk_data.title,
        description=risk_data.description,
        category=risk_data.category,
        probability=risk_data.probability,
        impact=risk_data.impact,
        severity=risk_data.severity,
        mitigation_plan=risk_data.mitigation_plan,
        status=risk_data.status,
    )
    db.add(risk)
    await db.commit()
    await db.refresh(risk)
    return risk


@router.get("", response_model=List[RiskResponse])
async def get_all_risks(
    db: AsyncSession = Depends(get_db)
):
    """Get all risks."""
    result = await db.execute(select(Risk).order_by(Risk.created_at.desc()))
    risks = result.scalars().all()
    return list(risks)


@router.get("/{project_id}", response_model=List[RiskResponse])
async def get_risks(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all risks for a project."""
    risks = await get_risks_by_project(db, project_id)
    return risks


@router.put("/{risk_id}", response_model=RiskResponse)
async def update_risk(
    risk_id: int,
    risk_data: RiskUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a risk."""
    result = await db.execute(select(Risk).where(Risk.id == risk_id))
    risk = result.scalar_one_or_none()
    
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    
    if risk_data.title is not None:
        risk.title = risk_data.title
    if risk_data.description is not None:
        risk.description = risk_data.description
    if risk_data.probability is not None:
        risk.probability = risk_data.probability
    if risk_data.impact is not None:
        risk.impact = risk_data.impact
    if risk_data.status is not None:
        risk.status = risk_data.status
    
    db.add(risk)
    await db.commit()
    await db.refresh(risk)
    return risk


@router.delete("/{risk_id}", status_code=204)
async def delete_risk(
    risk_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a risk."""
    result = await db.execute(select(Risk).where(Risk.id == risk_id))
    risk = result.scalar_one_or_none()
    
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    
    await db.delete(risk)
    await db.commit()
    return None


