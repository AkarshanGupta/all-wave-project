from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingUpload, MeetingResponse, MeetingCreate, MeetingUpdate
from app.services.meeting_service import create_meeting_from_text, get_meetings_by_project

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.post("/upload", response_model=MeetingResponse, status_code=201)
async def upload_meeting(
    meeting_data: MeetingUpload,
    db: AsyncSession = Depends(get_db)
):
    """Upload meeting text and process with LLM."""
    try:
        meeting = await create_meeting_from_text(db, meeting_data)
        return meeting
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=MeetingResponse, status_code=201)
async def create_meeting(
    meeting_data: MeetingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new meeting."""
    # First, verify the project exists
    from app.models.project import Project
    from datetime import datetime
    
    result = await db.execute(select(Project).where(Project.id == meeting_data.project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=404, 
            detail=f"Project with id {meeting_data.project_id} not found. Please create the project first."
        )
    
    # Convert date string to date object if provided
    date_obj = None
    if meeting_data.date:
        try:
            date_obj = datetime.strptime(meeting_data.date, "%Y-%m-%d").date()
        except:
            pass
    
    meeting = Meeting(
        project_id=meeting_data.project_id,
        title=meeting_data.title,
        raw_text=meeting_data.raw_text,
        summary=meeting_data.summary,
        date=date_obj,
        time=meeting_data.time,
        duration=meeting_data.duration,
        attendees=meeting_data.attendees,
        status=meeting_data.status or "scheduled",
    )
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    return meeting


@router.get("", response_model=List[MeetingResponse])
async def get_all_meetings(
    db: AsyncSession = Depends(get_db)
):
    """Get all meetings."""
    result = await db.execute(select(Meeting).order_by(Meeting.created_at.desc()))
    meetings = result.scalars().all()
    return list(meetings)


@router.get("/{project_id}", response_model=List[MeetingResponse])
async def get_meetings(
    project_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all meetings for a project."""
    meetings = await get_meetings_by_project(db, project_id)
    return meetings


@router.put("/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(
    meeting_id: int,
    meeting_data: MeetingUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a meeting."""
    from datetime import datetime
    
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    if meeting_data.title is not None:
        meeting.title = meeting_data.title
    if meeting_data.summary is not None:
        meeting.summary = meeting_data.summary
    if meeting_data.date is not None:
        try:
            meeting.date = datetime.strptime(meeting_data.date, "%Y-%m-%d").date()
        except:
            meeting.date = None
    if meeting_data.time is not None:
        meeting.time = meeting_data.time
    if meeting_data.duration is not None:
        meeting.duration = meeting_data.duration
    if meeting_data.attendees is not None:
        meeting.attendees = meeting_data.attendees
    if meeting_data.status is not None:
        meeting.status = meeting_data.status
    
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    return meeting


@router.delete("/{meeting_id}", status_code=204)
async def delete_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a meeting."""
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    await db.delete(meeting)
    await db.commit()
    return None


