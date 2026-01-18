from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ResourceSkill(Base):
    """Skills associated with resources for matching and optimization."""
    __tablename__ = "resource_skills"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = Column(String(100), nullable=False, index=True)
    proficiency_level = Column(Integer, nullable=False)  # 1-5 scale
    
    resource = relationship("Resource", back_populates="skills")
