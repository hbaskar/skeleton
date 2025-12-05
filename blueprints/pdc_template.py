import azure.functions as func
from schemas.pdc_template import PdcTemplateCreate, PdcTemplateUpdate, PdcTemplateOut
from services.pdc_template_service import (
    create_template, get_template, list_templates, update_template, delete_template
)
import json

bp = func.Blueprint()

@bp.route(route="pdc-template", methods=["POST"])
def create_pdc_template(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        schema = PdcTemplateCreate(**data)
        try:
            template = create_template(schema.dict())
            return func.HttpResponse(json.dumps(template.to_dict()), status_code=201)
        except ValueError as ve:
            return func.HttpResponse(str(ve), status_code=400)
        except Exception as e:
            return func.HttpResponse("Internal server error", status_code=500)

@bp.route(route="pdc-template/get", methods=["POST"])
def get_pdc_template(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        template_id = int(data.get("template_id"))
        template = get_template(template_id)
        if not template:
            return func.HttpResponse("Not found", status_code=404)
        return func.HttpResponse(json.dumps(template.to_dict()), status_code=200)

@bp.route(route="pdc-template/list", methods=["POST"])
def list_pdc_templates(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json() if req.get_body() else {}
        cursor = int(data.get('cursor', 0))
        limit = int(data.get('limit', 10))
        templates, next_cursor = list_templates(cursor=cursor, limit=limit)
        response = {
            'results': [t.to_dict() for t in templates],
            'next_cursor': next_cursor
        }
        return func.HttpResponse(json.dumps(response), status_code=200)

@bp.route(route="pdc-template/update", methods=["POST"])
def update_pdc_template(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        template_id = int(data.get("template_id"))
        schema = PdcTemplateUpdate(**data)
        try:
            template = update_template(template_id, schema.dict())
            if not template:
                return func.HttpResponse("Not found", status_code=404)
            return func.HttpResponse(json.dumps(template.to_dict()), status_code=200)
        except ValueError as ve:
            return func.HttpResponse(str(ve), status_code=400)
        except Exception as e:
            return func.HttpResponse("Internal server error", status_code=500)

@bp.route(route="pdc-template/delete", methods=["POST"])
def delete_pdc_template(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        template_id = int(data.get("template_id"))
        deleted_record = delete_template(template_id)
        if not deleted_record:
            return func.HttpResponse("Not found", status_code=404)
        return func.HttpResponse(json.dumps(deleted_record), status_code=200)
