from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class AllocationScenario(Base):
    """Store what-if scenarios for resource allocation analysis."""
    __tablename__ = "allocation_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    scenario_data = Column(JSON, nullable=False)  # Stores allocation configurations
    metrics = Column(JSON, nullable=True)  # Stores calculated metrics
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
