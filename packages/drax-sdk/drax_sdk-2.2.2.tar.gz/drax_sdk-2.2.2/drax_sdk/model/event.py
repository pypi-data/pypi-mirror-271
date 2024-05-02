from pydantic import BaseModel, Field
from typing import Optional, Dict


class Event(BaseModel):
    timestamp: int
    node: str
    project_id: str = Field(alias="projectId")
    type: str

    @classmethod
    def create(cls, type: str, project_id: str, node: str, params: Dict[str, str]):
        event = cls(type=type, project_id=project_id, node=node)
        for key, value in params.items():
            setattr(event, key, value)
        return event

    class Config:
        populate_by_name = True
