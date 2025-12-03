# Blueprint package initializer
from .pdc_template import register as register_pdc_template
from .pdc_class import register as register_pdc_class
from .http_trigger import register as register_http_trigger

def register(app):
    register_pdc_template(app)
    register_pdc_class(app)
    register_http_trigger(app)
