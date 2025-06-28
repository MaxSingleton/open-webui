import time
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from sqlalchemy import Column, Text, DateTime, func

from open_webui.internal.db import Base, get_db


class NotionIntegration(Base):
    __tablename__ = "notion_integration"
    project_id = Column(Text, primary_key=True)
    database_id = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class NotionIntegrationModel(BaseModel):
    project_id: str
    database_id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class NotionIntegrationTable:
    @staticmethod
    def get_by_project(project_id: str) -> Optional[NotionIntegrationModel]:
        with get_db() as db:
            row = db.query(NotionIntegration).filter_by(project_id=project_id).first()
            if not row:
                return None
            return NotionIntegrationModel.model_validate(row)

    @staticmethod
    def upsert(project_id: str, database_id: str) -> NotionIntegrationModel:
        with get_db() as db:
            row = db.query(NotionIntegration).filter_by(project_id=project_id).first()
            if row:
                row.database_id = database_id
            else:
                row = NotionIntegration(project_id=project_id, database_id=database_id)
                db.add(row)
            db.commit()
            db.refresh(row)
            return NotionIntegrationModel.model_validate(row)