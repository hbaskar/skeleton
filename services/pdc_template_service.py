from models.pdc_template import PdcTemplate, Base
from config.database import get_connection_string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
import datetime
from contextlib import contextmanager
from utils.pagination import paginate_query

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={get_connection_string()}")
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def create_template(data) -> PdcTemplate:
    import logging
    with get_session() as session:
        template = PdcTemplate(
            name=data['name'],
            created_by=data.get('created_by'),
            is_active=data.get('is_active', True)
        )
        # Set attributes from dict
        attrs = data.get('attributes', {})
        for i in range(1, 36):
            attr_name = f'attribute_{i}'
            setattr(template, attr_name, attrs.get(attr_name))
        session.add(template)
        logging.info(str(session.new))
        try:
            logging.info(str(session.query(PdcTemplate).filter(PdcTemplate.name == data['name'])))
            session.commit()
            session.refresh(template)
            return template
        except Exception as e:
            session.rollback()
            # Check for IntegrityError (duplicate name)
            if hasattr(e, 'orig') and hasattr(e.orig, 'args') and 'duplicate key' in str(e.orig.args):
                raise ValueError('A template with this name already exists.')
            raise

def get_template(template_id: int) -> Optional[PdcTemplate]:
    import logging
    with get_session() as session:
        query = session.query(PdcTemplate).filter(PdcTemplate.template_id == template_id)
        logging.info(str(query))
        template = query.first()
        return template

def list_templates(cursor: int = 0, limit: int = 10) -> tuple[list, int]:
    import logging
    with get_session() as session:
        # The actual query is inside paginate_query, so log the base query
        query = session.query(PdcTemplate)
        logging.info(str(query))
        templates, next_cursor = paginate_query(session, PdcTemplate, cursor_field='template_id', cursor=cursor, limit=limit)
        return templates, next_cursor

def update_template(template_id: int, data) -> Optional[PdcTemplate]:
    import logging
    with get_session() as session:
        query = session.query(PdcTemplate).filter(PdcTemplate.template_id == template_id)
        logging.info(str(query))
        template = query.first()
        if not template:
            return None
        # Check if any class uses this template
        from models.pdc_class import PdcClass
        class_count = session.query(PdcClass).filter(PdcClass.template_id == template_id).count()
     
        attrs = data.get('attributes')
        if attrs is None:
            attrs = {}
        # Only block if actual attribute fields are being updated
        if class_count > 0:
            for i in range(1, 36):
                attr_name = f'attribute_{i}'
                if attr_name in attrs and attrs[attr_name] is not None:
                    logging.error(f"Attempt to update {attr_name} when classes exist for template {template_id}")
                    raise ValueError('Cannot update template attributes: one or more classes use this template.')
        template.name = data.get('name', template.name)
        for i in range(1, 36):
            attr_name = f'attribute_{i}'
            # Only update attribute if present and not None
            if attr_name in attrs and attrs[attr_name] is not None:
                if class_count > 0:
                    continue  # skip attribute update if classes exist
                setattr(template, attr_name, attrs[attr_name])
        template.updated_at = datetime.datetime.utcnow()
        template.updated_by = data.get('updated_by', template.updated_by)
        template.is_active = data.get('is_active', template.is_active)
        try:
            session.commit()
            session.refresh(template)
            return template
        except Exception as e:
            session.rollback()
            logging.error(f"Error updating template {template_id}: {e}")
            # Check for IntegrityError (duplicate name)
            if hasattr(e, 'orig') and hasattr(e.orig, 'args') and 'duplicate key' in str(e.orig.args):
                raise ValueError('A template with this name already exists.')
            raise

def delete_template(template_id: int) -> bool:
    import logging
    with get_session() as session:
        query = session.query(PdcTemplate).filter(PdcTemplate.template_id == template_id)
        logging.info(str(query))
        template = query.first()
        if template:
            deleted_data = template.to_dict() if hasattr(template, 'to_dict') else None
            session.delete(template)
            session.commit()
            return deleted_data
        return None
