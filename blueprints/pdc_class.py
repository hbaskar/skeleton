import azure.functions as func
from schemas.pdc_class import PdcClassCreate, PdcClassUpdate, PdcClassOut
from services.pdc_class_service import (
    create_class, get_class, list_classes, update_class, delete_class
)
import json

bp = func.Blueprint()

@bp.route(route="odc-class/blank", methods=["POST"])
def get_blank_odc_class(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        template_id = int(data.get("template_id"))
        from models.pdc_template import PdcTemplate
        from models.pdc_template_field import PdcTemplateField
        from config.database import get_connection_string
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={get_connection_string()}")
        SessionLocal = sessionmaker(bind=engine)
        with SessionLocal() as session:
            template_obj = session.query(PdcTemplate).filter(PdcTemplate.template_id == template_id).first()
            if not template_obj:
                return func.HttpResponse("Template not found", status_code=404)
            # Get all attribute names from template (attribute_1 ... attribute_35)
            template_attrs = {}
            fields = session.query(PdcTemplateField).filter(PdcTemplateField.template_id == template_id).all()
            template_attrs = {}
            metadata_keys = {field.metadata_key: field for field in fields}
            for i in range(1, 36):
                attr_name = f'attribute_{i}'
                key = getattr(template_obj, attr_name)
                # Only include if key matches a metadata_key in template_fields
                if key and key in metadata_keys:
                    field = metadata_keys[key]
                    template_attrs[key] = {
                        "display_name": field.display_name,
                        "data_type": field.data_type,
                        "is_required": field.is_required,
                        "default_value": field.default_value,
                        "validation_rule": field.validation_rule,
                        "sort_order": field.sort_order,
                        "is_active": field.is_active,
                        "lookup_type": getattr(field, "lookup_type", None)
                    }
            blank_record = {
                "class_id": None,
                "template_id": template_id,
                "name": None,
                "attributes": template_attrs,
                "created_at": None,
                "created_by": None,
                "updated_at": None,
                "updated_by": None,
                "is_active": True
            }
        return func.HttpResponse(json.dumps(blank_record), status_code=200)
    
@bp.route(route="pdc-class/blank", methods=["POST"])
def get_blank_pdc_class(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        template_id = int(data.get("template_id"))
        from models.pdc_template import PdcTemplate
        from config.database import get_connection_string
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={get_connection_string()}")
        SessionLocal = sessionmaker(bind=engine)
        with SessionLocal() as session:
            template_obj = session.query(PdcTemplate).filter(PdcTemplate.template_id == template_id).first()
            if not template_obj:
                return func.HttpResponse("Template not found", status_code=404)
            # Build blank attributes dict using template attribute names
            attr_names = [getattr(template_obj, f'attribute_{i}') for i in range(1, 36)]
            attributes = {name: None for name in attr_names if name}
            blank_record = {
                "class_id": None,
                "template_id": template_id,
                "name": None,
                "attributes": attributes,
                "created_at": None,
                "created_by": None,
                "updated_at": None,
                "updated_by": None,
                "is_active": True
            }
        return func.HttpResponse(json.dumps(blank_record), status_code=200)
    
@bp.route(route="pdc-class", methods=["POST"])
def create_pdc_class(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        schema = PdcClassCreate(**data)
        try:
            pdc_class = create_class(schema.dict())
            # Fetch template for attribute names for response
            from models.pdc_template import PdcTemplate
            from config.database import get_connection_string
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            engine = create_engine(f"mssql+pyodbc:///?odbc_connect={get_connection_string()}")
            SessionLocal = sessionmaker(bind=engine)
            with SessionLocal() as session:
                template_obj = session.query(PdcTemplate).filter(PdcTemplate.template_id == pdc_class.template_id).first()
            return func.HttpResponse(json.dumps(pdc_class.to_dict(template_obj)), status_code=201)
        except Exception as e:
            import traceback
            return func.HttpResponse(f"Internal server error: {str(e)}\n{traceback.format_exc()}", status_code=500)

@bp.route(route="pdc-class/get", methods=["POST"])
def get_pdc_class(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        class_id = int(data.get("class_id"))
        pdc_class = get_class(class_id)
        if not pdc_class:
            return func.HttpResponse("Not found", status_code=404)
        # Fetch template for attribute names
        from models.pdc_template import PdcTemplate
        from config.database import get_connection_string
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={get_connection_string()}")
        SessionLocal = sessionmaker(bind=engine)
        with SessionLocal() as session:
            template_obj = session.query(PdcTemplate).filter(PdcTemplate.template_id == pdc_class.template_id).first()
        return func.HttpResponse(json.dumps(pdc_class.to_dict(template_obj)), status_code=200)

@bp.route(route="pdc-class/list", methods=["POST"])
def list_pdc_classes(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json() if req.get_body() else {}
        cursor = int(data.get('cursor', 0))
        limit = int(data.get('limit', 10))
        classes, next_cursor = list_classes(cursor=cursor, limit=limit)
        from models.pdc_template import PdcTemplate
        from config.database import get_connection_string
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={get_connection_string()}")
        SessionLocal = sessionmaker(bind=engine)
        results = []
        with SessionLocal() as session:
            for c in classes:
                template_obj = session.query(PdcTemplate).filter(PdcTemplate.template_id == c.template_id).first()
                results.append(c.to_dict(template_obj))
        response = {
            'results': results,
            'next_cursor': next_cursor
        }
        return func.HttpResponse(json.dumps(response), status_code=200)

@bp.route(route="pdc-class/update", methods=["POST"])
def update_pdc_class(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        class_id = int(data.get("class_id"))
        schema = PdcClassUpdate(**data)
        pdc_class = update_class(class_id, schema.dict())
        if not pdc_class:
            return func.HttpResponse("Not found", status_code=404)
        # Fetch template for attribute names for response
        from models.pdc_template import PdcTemplate
        from config.database import get_connection_string
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={get_connection_string()}")
        SessionLocal = sessionmaker(bind=engine)
        with SessionLocal() as session:
            template_obj = session.query(PdcTemplate).filter(PdcTemplate.template_id == pdc_class.template_id).first()
        return func.HttpResponse(json.dumps(pdc_class.to_dict(template_obj)), status_code=200)

@bp.route(route="pdc-class/delete", methods=["POST"])
def delete_pdc_class(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        class_id = int(data.get("class_id"))
        deleted_record = delete_class(class_id)
        if not deleted_record:
            return func.HttpResponse("Not found", status_code=404)
        return func.HttpResponse(json.dumps(deleted_record), status_code=200)
