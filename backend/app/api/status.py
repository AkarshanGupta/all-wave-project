from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.status_report import StatusReport
from app.schemas.status_report import StatusReportResponse
from app.services.status_service import generate_status_report, get_status_report_by_project

router = APIRouter(prefix="/status", tags=["status"])


@router.post("/generate/{project_id}", response_model=StatusReportResponse, status_code=201)
async def generate_status(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Generate status report for a project."""
    try:
        status_report = await generate_status_report(db, project_id)
        return status_report
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}", response_model=StatusReportResponse)
async def get_status(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get the latest status report for a project."""
    status_report = await get_status_report_by_project(db, project_id)
    
    if not status_report:
        raise HTTPException(status_code=404, detail="Status report not found")
    
    return status_report

