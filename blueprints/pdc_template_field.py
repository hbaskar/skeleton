import azure.functions as func
import json
from schemas.pdc_template_field import (
    PdcTemplateFieldCreate, PdcTemplateFieldUpdate, PdcTemplateFieldOut
)
from services.pdc_template_field_service import (
    create_template_field, get_template_field, list_template_fields,
    update_template_field, delete_template_field
)


bp = func.Blueprint()

# CREATE
@bp.route(route="pdc-template-field/create", methods=["POST"])
def create_pdc_template_field(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    data = req.get_json()
    try:
        schema = PdcTemplateFieldCreate(**data)
        field = create_template_field(schema.dict())
        return func.HttpResponse(json.dumps(field.to_dict()), status_code=201)
    except ValueError as ve:
        return func.HttpResponse(str(ve), status_code=400)

# READ
@bp.route(route="pdc-template-field/get", methods=["GET"])
def get_pdc_template_field(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        field_id = int(req.params.get("template_field_id"))
        field = get_template_field(field_id)
        if not field:
            return func.HttpResponse("Not found", status_code=404)
        return func.HttpResponse(json.dumps(field.to_dict()), status_code=200)

# LIST
@bp.route(route="pdc-template-field/list", methods=["GET"])
def list_pdc_template_fields(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        template_id = req.params.get("template_id")
        fields = list_template_fields(int(template_id) if template_id else None)
        return func.HttpResponse(json.dumps([f.to_dict() for f in fields]), status_code=200)

# UPDATE
@bp.route(route="pdc-template-field/update", methods=["POST"])
def update_pdc_template_field(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    data = req.get_json()
    field_id = int(data.get("template_field_id"))
    schema = PdcTemplateFieldUpdate(**data)
    update_data = schema.model_dump(exclude_none=True)
    update_data.pop("template_field_id", None)
    field = update_template_field(field_id, update_data)
    if not field:
        return func.HttpResponse("Not found", status_code=404)
    return func.HttpResponse(json.dumps(field.to_dict()), status_code=200)

# DELETE
@bp.route(route="pdc-template-field/delete", methods=["POST"])
def delete_pdc_template_field(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        field_id = int(data.get("template_field_id"))
        success = delete_template_field(field_id)
        if not success:
            return func.HttpResponse("Not found", status_code=404)
        return func.HttpResponse("Deleted", status_code=200)
