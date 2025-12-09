from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PdcTemplateFieldBase(BaseModel):
    template_id: int
    metadata_key: str
    display_name: Optional[str] = None
    data_type: Optional[str] = None
    is_required: Optional[bool] = False
    default_value: Optional[str] = None
    validation_rule: Optional[str] = None
    sort_order: Optional[int] = None
    lookup_type: Optional[str] = None
    lookup_url: Optional[str] = None
    description: Optional[str] = None
    group_header: Optional[str] = None
    is_active: Optional[bool] = True

class PdcTemplateFieldCreate(PdcTemplateFieldBase):
    created_by: str

class PdcTemplateFieldUpdate(BaseModel):
    template_field_id: int
    template_id: Optional[int] = None
    metadata_key: Optional[str] = None
    display_name: Optional[str] = None
    data_type: Optional[str] = None
    is_required: Optional[bool] = None
    default_value: Optional[str] = None
    validation_rule: Optional[str] = None
    sort_order: Optional[int] = None
    lookup_type: Optional[str] = None
    lookup_url: Optional[str] = None
    description: Optional[str] = None
    group_header: Optional[str] = None
    is_active: Optional[bool] = None
    modified_by: Optional[str] = None

class PdcTemplateFieldOut(PdcTemplateFieldBase):
    template_field_id: int
    created_at: datetime
    created_by: str
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None
