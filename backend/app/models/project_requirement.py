from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProjectRequirement(Base):
    """Skills and resources required for projects."""
    __tablename__ = "project_requirements"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    required_proficiency = Column(Integer, nullable=False)  # 1-5 scale
    required_hours = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    
    project = relationship("Project", back_populates="requirements")
