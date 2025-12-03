from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PdcTemplateBase(BaseModel):
    name: str
    attributes: Optional[dict] = None  # {"attribute_1": "A1", "attribute_3": "A3"}
    is_active: Optional[bool] = True

class PdcTemplateCreate(PdcTemplateBase):
    created_by: Optional[str] = None

class PdcTemplateUpdate(PdcTemplateBase):
    updated_by: Optional[str] = None

class PdcTemplateOut(PdcTemplateBase):
    template_id: int
    created_at: datetime
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
