from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Risk(Base):
    __tablename__ = "risks"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    probability = Column(Integer, nullable=False)
    impact = Column(Integer, nullable=False)
    severity = Column(String(50), nullable=False)
    mitigation_plan = Column(Text, nullable=True)
    status = Column(String(50), default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # New columns - nullable so queries work if they don't exist yet
    risk_score = Column(Float, nullable=True, default=None)
    trend = Column(String(20), nullable=True, default="stable")
    approval_status = Column(String(50), nullable=True, default="pending")
    approved_by = Column(String(255), nullable=True)
    is_escalated = Column(Integer, nullable=True, default=0)

    project = relationship("Project", back_populates="risks")
    metrics = relationship("RiskMetric", back_populates="risk", cascade="all, delete-orphan")





