from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    probability = Column(Integer, nullable=False)
    impact = Column(Integer, nullable=False)
    severity = Column(String(50), nullable=False)
    risk_score = Column(Float, nullable=True, default=None)  # Will be populated after migration
    trend = Column(String(20), default="stable", nullable=True)  # Will be populated after migration
    mitigation_plan = Column(Text, nullable=True)
    status = Column(String(50), default="open")
    approval_status = Column(String(50), default="pending", nullable=True)  # Will be populated after migration
    approved_by = Column(String(255), nullable=True)
    is_escalated = Column(Integer, default=0, nullable=True)  # Will be populated after migration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="risks")
    metrics = relationship("RiskMetric", back_populates="risk", cascade="all, delete-orphan")



