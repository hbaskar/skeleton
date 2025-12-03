import azure.functions as func
from typing import Any

def register(app):
    @app.function_name(name="HttpExample")
    @app.route(route="HttpExample", methods=["GET", "POST"])
    def http_example(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
        name = req.params.get('name')
        if not name:
            try:
                req_body = req.get_json()
            except ValueError:
                req_body = None
            if req_body:
                name = req_body.get('name')
        return func.HttpResponse(f"Hello, {name or 'World'}!", status_code=200)
