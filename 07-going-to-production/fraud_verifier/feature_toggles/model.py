from typing import Any

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()


class FeatureModel(Base):
    __tablename__ = "feature_toggles"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    enabled = Column(Boolean)
