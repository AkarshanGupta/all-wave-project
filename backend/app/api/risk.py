from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict
from app.core.database import get_db
from app.models.risk import Risk
from app.schemas.risk import RiskAnalyze, RiskResponse, RiskCreate, RiskUpdate, RiskAnalyticsResponse, RiskMatrixDataResponse
from app.services.risk_service import analyze_risks_from_text, get_risks_by_project, analyze_project_documentation
from app.services.risk_analytics_service import (
    get_risk_analytics, 
    calculate_trend, 
    detect_early_warnings,
    calculate_risk_score,
    record_risk_metric
)

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


@router.post("/analyze-project/{project_id}", response_model=List[RiskResponse], status_code=201)
async def analyze_project_docs(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Automatically analyze all project documentation (status reports, resources, allocations) for risks."""
    try:
        risks = await analyze_project_documentation(db, project_id)
        return risks
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/{project_id}", response_model=RiskAnalyticsResponse)
async def get_analytics(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get risk analytics for a project."""
    try:
        analytics = await get_risk_analytics(db, project_id)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matrix/{project_id}", response_model=RiskMatrixDataResponse)
async def get_risk_matrix(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get risk matrix data (probability vs impact)."""
    try:
        risks = await get_risks_by_project(db, project_id)
        risk_responses = [RiskResponse.from_orm(r) for r in risks]
        return RiskMatrixDataResponse(
            risks=risk_responses,
            probability_range=(1, 10),
            impact_range=(1, 10)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/warnings/{project_id}", response_model=List[Dict])
async def get_early_warnings(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get early warning indicators for escalation."""
    try:
        warnings = await detect_early_warnings(db, project_id)
        return warnings
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
    
    # Calculate risk score
    risk_score = calculate_risk_score(risk_data.probability, risk_data.impact)
    
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
        risk_score=risk_score,
        trend="stable",
    )
    db.add(risk)
    await db.commit()
    await db.refresh(risk)
    
    # Record initial metric for trend analysis
    await record_risk_metric(db, risk.id, risk.probability, risk.impact, risk.severity)
    await db.commit()
    
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
    
    # Track if probability or impact changed for recalculation
    needs_score_recalc = False
    
    if risk_data.title is not None:
        risk.title = risk_data.title
    if risk_data.description is not None:
        risk.description = risk_data.description
    if risk_data.category is not None:
        risk.category = risk_data.category
    if risk_data.severity is not None:
        risk.severity = risk_data.severity
    if risk_data.mitigation_plan is not None:
        risk.mitigation_plan = risk_data.mitigation_plan
    if risk_data.probability is not None:
        risk.probability = risk_data.probability
        needs_score_recalc = True
    if risk_data.impact is not None:
        risk.impact = risk_data.impact
        needs_score_recalc = True
    if risk_data.status is not None:
        risk.status = risk_data.status
    if risk_data.approval_status is not None:
        risk.approval_status = risk_data.approval_status
    if risk_data.approved_by is not None:
        risk.approved_by = risk_data.approved_by
    
    # Recalculate risk score if probability or impact changed
    if needs_score_recalc:
        risk.risk_score = calculate_risk_score(risk.probability, risk.impact)
        # Record metric for trend analysis
        await record_risk_metric(db, risk.id, risk.probability, risk.impact, risk.severity)
        # Update trend
        risk.trend = await calculate_trend(db, risk.id)
    
    db.add(risk)
    await db.commit()
    await db.refresh(risk)
    return risk


@router.post("/{risk_id}/approve")
async def approve_risk(
    risk_id: int,
    approved_by: str,
    db: AsyncSession = Depends(get_db)
):
    """Approve a risk and record the metric."""
    result = await db.execute(select(Risk).where(Risk.id == risk_id))
    risk = result.scalar_one_or_none()
    
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    
    risk.approval_status = "approved"
    risk.approved_by = approved_by
    db.add(risk)
    await db.commit()
    await db.refresh(risk)
    
    # Record metric snapshot
    await record_risk_metric(db, risk_id, risk.probability, risk.impact, risk.severity)
    
    return {"status": "approved", "risk_id": risk_id}


@router.post("/{risk_id}/reject")
async def reject_risk(
    risk_id: int,
    approved_by: str,
    db: AsyncSession = Depends(get_db)
):
    """Reject a risk."""
    result = await db.execute(select(Risk).where(Risk.id == risk_id))
    risk = result.scalar_one_or_none()
    
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    
    risk.approval_status = "rejected"
    risk.approved_by = approved_by
    db.add(risk)
    await db.commit()
    await db.refresh(risk)
    
    return {"status": "rejected", "risk_id": risk_id}


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
