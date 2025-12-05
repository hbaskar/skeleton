import os
import datetime
from contextlib import contextmanager
from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.database import get_connection_string
from models import Base
from models.pdc_template_field import PdcTemplateField
from models.pdc_template import PdcTemplate


engine = create_engine(f"mssql+pyodbc:///?odbc_connect={get_connection_string()}")
SessionLocal = sessionmaker(bind=engine)
# Ensure all tables are created (for dev/migration only; remove in prod)
Base.metadata.create_all(engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def create_template_field(data) -> PdcTemplateField:
    with get_session() as session:
        # Validate metadata_key matches one of the template's defined attributes (non-empty value)
        template = session.query(PdcTemplate).filter(PdcTemplate.template_id == data['template_id']).first()
        if not template:
            raise ValueError("Template not found")
        attribute_values = [getattr(template, f"attribute_{i}") for i in range(1, 36)]
        allowed = {val for val in attribute_values if val not in (None, "", " ")}
        if data['metadata_key'] not in allowed:
            raise ValueError("metadata_key must reference an existing template attribute value")

        # Auto-construct lookup_url when not provided
        if not data.get('lookup_url'):
            base_lookup_url = os.getenv('AZURE_LOOKUP_URL', '').rstrip('/')
            lookup_type = data.get('lookup_type')
            if base_lookup_url and lookup_type:
                data['lookup_url'] = f"{base_lookup_url}/{lookup_type}"
        field = PdcTemplateField(
            template_id=data['template_id'],
            metadata_key=data['metadata_key'],
            display_name=data.get('display_name'),
            data_type=data.get('data_type'),
            is_required=data.get('is_required', False),
            default_value=data.get('default_value'),
            validation_rule=data.get('validation_rule'),
            sort_order=data.get('sort_order'),
            lookup_type=data.get('lookup_type'),
            lookup_url=data.get('lookup_url'),
            is_active=data.get('is_active', True),
            created_at=datetime.datetime.utcnow(),
            created_by=data['created_by']
        )
        session.add(field)
        session.commit()
        session.refresh(field)
        return field

def get_template_field(field_id: int) -> Optional[PdcTemplateField]:
    with get_session() as session:
        field = session.query(PdcTemplateField).filter(PdcTemplateField.template_field_id == field_id).first()
        return field

def list_template_fields(template_id: Optional[int] = None) -> List[PdcTemplateField]:
    with get_session() as session:
        query = session.query(PdcTemplateField)
        if template_id:
            query = query.filter(PdcTemplateField.template_id == template_id)
        return query.all()

def update_template_field(field_id: int, data) -> Optional[PdcTemplateField]:
    with get_session() as session:
        field = session.query(PdcTemplateField).filter(PdcTemplateField.template_field_id == field_id).first()
        if not field:
            return None
        for key, value in data.items():
            if hasattr(field, key):
                setattr(field, key, value)
        field.modified_at = datetime.datetime.utcnow()
        field.modified_by = data.get('modified_by', field.modified_by)
        session.commit()
        session.refresh(field)
        return field

def delete_template_field(field_id: int) -> bool:
    with get_session() as session:
        field = session.query(PdcTemplateField).filter(PdcTemplateField.template_field_id == field_id).first()
        if field:
            session.delete(field)
            session.commit()
            return True
        return False
