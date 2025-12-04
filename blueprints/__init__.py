# Blueprint package initializer

from .pdc_template import register as register_pdc_template
from .pdc_class import register as register_pdc_class
from .http_trigger import register as register_http_trigger
from .pdc_template_field import register as register_pdc_template_field

def register(app):
    register_pdc_template(app)
    register_pdc_class(app)
    register_http_trigger(app)
    register_pdc_template_field(app)
