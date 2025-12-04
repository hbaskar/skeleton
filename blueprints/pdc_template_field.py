import azure.functions as func
import json
from schemas.pdc_template_field import (
    PdcTemplateFieldCreate, PdcTemplateFieldUpdate, PdcTemplateFieldOut
)
from services.pdc_template_field_service import (
    create_template_field, get_template_field, list_template_fields,
    update_template_field, delete_template_field
)


def register(app):
    # CREATE
    @app.function_name(name="CreatePdcTemplateField")
    @app.route(route="pdc-template-field/create", methods=["POST"])
    def create_pdc_template_field(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        schema = PdcTemplateFieldCreate(**data)
        field = create_template_field(schema.dict())
        return func.HttpResponse(json.dumps(field.to_dict()), status_code=201)

    # READ
    @app.function_name(name="GetPdcTemplateField")
    @app.route(route="pdc-template-field/get", methods=["GET"])
    def get_pdc_template_field(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        field_id = int(req.params.get("template_field_id"))
        field = get_template_field(field_id)
        if not field:
            return func.HttpResponse("Not found", status_code=404)
        return func.HttpResponse(json.dumps(field.to_dict()), status_code=200)

    # LIST
    @app.function_name(name="ListPdcTemplateFields")
    @app.route(route="pdc-template-field/list", methods=["GET"])
    def list_pdc_template_fields(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        template_id = req.params.get("template_id")
        fields = list_template_fields(int(template_id) if template_id else None)
        return func.HttpResponse(json.dumps([f.to_dict() for f in fields]), status_code=200)

    # UPDATE
    @app.function_name(name="UpdatePdcTemplateField")
    @app.route(route="pdc-template-field/update", methods=["POST"])
    def update_pdc_template_field(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        field_id = int(data.get("template_field_id"))
        schema = PdcTemplateFieldUpdate(**data)
        field = update_template_field(field_id, schema.dict())
        if not field:
            return func.HttpResponse("Not found", status_code=404)
        return func.HttpResponse(json.dumps(field.to_dict()), status_code=200)

    # DELETE
    @app.function_name(name="DeletePdcTemplateField")
    @app.route(route="pdc-template-field/delete", methods=["POST"])
    def delete_pdc_template_field(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        data = req.get_json()
        field_id = int(data.get("template_field_id"))
        success = delete_template_field(field_id)
        if not success:
            return func.HttpResponse("Not found", status_code=404)
        return func.HttpResponse("Deleted", status_code=200)
