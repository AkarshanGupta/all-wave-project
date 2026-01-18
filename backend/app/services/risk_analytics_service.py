from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from typing import List, Dict
from app.models.risk import Risk
from app.models.risk_metric import RiskMetric
from app.schemas.risk import RiskAnalyticsResponse


def calculate_risk_score(probability: int, impact: int) -> float:
    """Calculate risk score from 0-100."""
    return (probability * impact / 100) * 100


async def record_risk_metric(
    db: AsyncSession,
    risk_id: int,
    probability: int,
    impact: int,
    severity: str
) -> None:
    """Record a metric snapshot for trend analysis."""
    risk_score = calculate_risk_score(probability, impact)
    metric = RiskMetric(
        risk_id=risk_id,
        probability=probability,
        impact=impact,
        risk_score=risk_score,
        severity=severity,
    )
    db.add(metric)
    await db.flush()


async def calculate_trend(
    db: AsyncSession,
    risk_id: int,
    days: int = 30
) -> str:
    """Calculate risk trend based on historical metrics."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(RiskMetric)
        .where(
            and_(
                RiskMetric.risk_id == risk_id,
                RiskMetric.recorded_at >= cutoff_date
            )
        )
        .order_by(RiskMetric.recorded_at)
    )
    metrics = list(result.scalars().all())
    
    if len(metrics) < 2:
        return "stable"
    
    # Compare first and last risk scores
    first_score = metrics[0].risk_score
    last_score = metrics[-1].risk_score
    
    diff_percent = ((last_score - first_score) / first_score * 100) if first_score > 0 else 0
    
    if diff_percent > 10:
        return "increasing"
    elif diff_percent < -10:
        return "decreasing"
    else:
        return "stable"


async def get_risk_analytics(
    db: AsyncSession,
    project_id: int
) -> RiskAnalyticsResponse:
    """Get comprehensive risk analytics for a project."""
    result = await db.execute(
        select(Risk).where(Risk.project_id == project_id)
    )
    risks = list(result.scalars().all())
    
    if not risks:
        return RiskAnalyticsResponse(
            total_risks=0,
            high_severity_count=0,
            escalated_count=0,
            approval_pending=0,
            average_risk_score=0,
            risks_by_category={},
            risks_by_severity={},
            risks_by_status={},
        )
    
    # Calculate metrics
    high_severity = len([r for r in risks if r.severity == "high"])
    escalated = len([r for r in risks if r.is_escalated])
    pending_approval = len([r for r in risks if r.approval_status == "pending"])
    
    avg_score = sum([r.risk_score or 0 for r in risks]) / len(risks)
    
    # Group by category
    category_counts = {}
    for risk in risks:
        category_counts[risk.category] = category_counts.get(risk.category, 0) + 1
    
    # Group by severity
    severity_counts = {}
    for risk in risks:
        severity_counts[risk.severity] = severity_counts.get(risk.severity, 0) + 1
    
    # Group by status
    status_counts = {}
    for risk in risks:
        status_counts[risk.status] = status_counts.get(risk.status, 0) + 1
    
    return RiskAnalyticsResponse(
        total_risks=len(risks),
        high_severity_count=high_severity,
        escalated_count=escalated,
        approval_pending=pending_approval,
        average_risk_score=round(avg_score, 2),
        risks_by_category=category_counts,
        risks_by_severity=severity_counts,
        risks_by_status=status_counts,
    )


async def detect_early_warnings(
    db: AsyncSession,
    project_id: int
) -> List[Dict]:
    """Detect risks that need escalation."""
    result = await db.execute(
        select(Risk).where(Risk.project_id == project_id)
    )
    risks = list(result.scalars().all())
    
    warnings = []
    for risk in risks:
        score = risk.risk_score or calculate_risk_score(risk.probability, risk.impact)
        
        # Escalate if high score and pending approval
        if score > 70 and risk.approval_status == "pending":
            warnings.append({
                "risk_id": risk.id,
                "title": risk.title,
                "reason": "High-risk item pending approval",
                "severity": "critical",
            })
        
        # Escalate if trend is increasing
        if risk.trend == "increasing":
            warnings.append({
                "risk_id": risk.id,
                "title": risk.title,
                "reason": "Risk score trending upward",
                "severity": "warning",
            })
    
    return warnings
