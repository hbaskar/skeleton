

import azure.functions as func
from blueprints.pdc_template import bp as pdc_template_bp
from blueprints.pdc_class import bp as pdc_class_bp
from blueprints.pdc_template_field import bp as pdc_template_field_bp


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Register blueprints using the blueprint pattern
app.register_blueprint(pdc_template_bp)
app.register_blueprint(pdc_class_bp)
app.register_blueprint(pdc_template_field_bp)


# import azure.functions as func
# from blueprints import register
# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
# register(app)