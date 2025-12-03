import azure.functions as func
from blueprints import register

app = func.FunctionApp()

# Register all blueprints
register(app)
