import azure.functions as func
from blueprints import http_trigger, pdc_template, pdc_class, pdc_template_field

app = func.FunctionApp()

# Register blueprints
http_trigger.register(app)
pdc_template.register(app)
pdc_class.register(app)
pdc_template_field.register(app)
