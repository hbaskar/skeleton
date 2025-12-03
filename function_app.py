import azure.functions as func
from blueprints import http_trigger, pdc_template, pdc_class

app = func.FunctionApp()

# Register blueprints
http_trigger.register(app)
pdc_template.register(app)
pdc_class.register(app)
