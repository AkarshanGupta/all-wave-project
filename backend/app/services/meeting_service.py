from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.models.meeting import Meeting, ActionItem
from app.schemas.meeting import MeetingUpload
from app.ai.llm_client import call_llm
from app.utils.file_utils import load_prompt
from datetime import datetime


async def create_meeting_from_text(
    db: AsyncSession,
    meeting_data: MeetingUpload
) -> Meeting:
    """Process meeting text through LLM and create meeting record."""
    prompt_template = load_prompt("meeting_prompt")
    prompt = prompt_template.format(meeting_text=meeting_data.raw_text)
    
    system_prompt = "You are an expert meeting analyst. Always return valid JSON."
    
    llm_response = await call_llm(prompt, system_prompt=system_prompt)
    
    meeting = Meeting(
        project_id=meeting_data.project_id,
        title=meeting_data.title,
        raw_text=meeting_data.raw_text,
        summary=llm_response.get("summary"),
        decisions=llm_response.get("decisions"),
        open_questions=llm_response.get("open_questions"),
    )
    
    db.add(meeting)
    await db.flush()
    
    action_items_data = llm_response.get("action_items", [])
    for item_data in action_items_data:
        due_date = None
        if item_data.get("due_date"):
            try:
                due_date = datetime.fromisoformat(item_data["due_date"].replace("Z", "+00:00"))
            except:
                pass
        
        action_item = ActionItem(
            meeting_id=meeting.id,
            description=item_data.get("description", ""),
            assignee=item_data.get("assignee"),
            due_date=due_date,
            status="open",
        )
        db.add(action_item)
    
    await db.commit()
    await db.refresh(meeting)
    
    return meeting


async def get_meetings_by_project(
    db: AsyncSession,
    project_id: int
) -> List[Meeting]:
    """Get all meetings for a project."""
    result = await db.execute(
        select(Meeting)
        .where(Meeting.project_id == project_id)
        .order_by(Meeting.created_at.desc())
    )
    meetings = result.scalars().all()
    
    for meeting in meetings:
        result = await db.execute(
            select(ActionItem)
            .where(ActionItem.meeting_id == meeting.id)
        )
        meeting.action_items = list(result.scalars().all())
    
    return meetings

