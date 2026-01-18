from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class RiskMetric(Base):
    """Track historical risk metrics for trend analysis."""
    __tablename__ = "risk_metrics"

    id = Column(Integer, primary_key=True, index=True)
    risk_id = Column(Integer, ForeignKey("risks.id", ondelete="CASCADE"), nullable=False, index=True)
    probability = Column(Integer, nullable=False)
    impact = Column(Integer, nullable=False)
    risk_score = Column(Float, nullable=False)
    severity = Column(String(50), nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    risk = relationship("Risk", back_populates="metrics")
