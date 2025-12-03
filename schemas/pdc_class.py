from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PdcClassCreate(BaseModel):
    template_id: int
    name: str
    attributes: Optional[dict] = Field(default_factory=dict)  # {template_attr_name: value}
    created_by: Optional[str]
    is_active: Optional[bool] = True

class PdcClassUpdate(BaseModel):
    class_id: int
    name: Optional[str]
    attributes: Optional[dict] = Field(default_factory=dict)  # {template_attr_name: value}
    updated_by: Optional[str]
    is_active: Optional[bool]

class PdcClassOut(BaseModel):
    class_id: int
    template_id: int
    name: str
    attributes: List[Optional[str]]
    created_at: Optional[datetime]
    created_by: Optional[str]
    updated_at: Optional[datetime]
    updated_by: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True
