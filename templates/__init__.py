import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def render(template, context):
    return JINJA_ENVIRONMENT.get_template(template + '.html').render(context)
