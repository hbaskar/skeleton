from models.pdc_class import PdcClass, Base
from config.database import get_connection_string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
import datetime
from contextlib import contextmanager
from utils.pagination import paginate_query
import logging

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={get_connection_string()}")
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def create_class(data) -> PdcClass:
    from models.pdc_template import PdcTemplate
    with get_session() as session:
        template_obj = session.query(PdcTemplate).filter(PdcTemplate.template_id == data['template_id']).first()
        if not template_obj:
            raise Exception('Template not found')
        attr_kwargs = PdcClass.from_template_and_data(template_obj, data.get('attributes', {}))
        pdc_class = PdcClass(
            template_id=data['template_id'],
            name=data['name'],
            created_by=data.get('created_by'),
            is_active=data.get('is_active', True),
            **attr_kwargs
        )
        session.add(pdc_class)
        logging.info(str(session.new))
        try:
            session.commit()
            session.refresh(pdc_class)
            return pdc_class
        except Exception as e:
            session.rollback()
            raise

def get_class(class_id: int) -> Optional[PdcClass]:
    with get_session() as session:
        query = session.query(PdcClass).filter(PdcClass.class_id == class_id)
        logging.info(str(query))
        pdc_class = query.first()
        return pdc_class

def list_classes(cursor: int = 0, limit: int = 10) -> tuple[list, int]:
    with get_session() as session:
        query = session.query(PdcClass)
        logging.info(str(query))
        classes, next_cursor = paginate_query(session, PdcClass, cursor_field='class_id', cursor=cursor, limit=limit)
        return classes, next_cursor

def update_class(class_id: int, data) -> Optional[PdcClass]:
    from models.pdc_template import PdcTemplate
    with get_session() as session:
        query = session.query(PdcClass).filter(PdcClass.class_id == class_id)
        logging.info(str(query))
        pdc_class = query.first()
        if not pdc_class:
            return None
        pdc_class.name = data.get('name', pdc_class.name)
        # Fetch template for mapping
        template_obj = session.query(PdcTemplate).filter(PdcTemplate.template_id == pdc_class.template_id).first()
        if template_obj and 'attributes' in data:
            attr_kwargs = PdcClass.from_template_and_data(template_obj, data['attributes'])
            for field, value in attr_kwargs.items():
                setattr(pdc_class, field, value)
        pdc_class.updated_at = datetime.datetime.utcnow()
        pdc_class.updated_by = data.get('updated_by', pdc_class.updated_by)
        pdc_class.is_active = data.get('is_active', pdc_class.is_active)
        session.commit()
        session.refresh(pdc_class)
        return pdc_class

def delete_class(class_id: int) -> Optional[dict]:
    with get_session() as session:
        query = session.query(PdcClass).filter(PdcClass.class_id == class_id)
        logging.info(str(query))
        pdc_class = query.first()
        if pdc_class:
            deleted_data = pdc_class.to_dict() if hasattr(pdc_class, 'to_dict') else None
            session.delete(pdc_class)
            session.commit()
            return deleted_data
        return None
