from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class StatusReport(Base):
    __tablename__ = "status_reports"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    executive_summary = Column(Text, nullable=False)
    risks_summary = Column(Text, nullable=True)
    meetings_summary = Column(Text, nullable=True)
    resources_summary = Column(Text, nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="status_reports")

