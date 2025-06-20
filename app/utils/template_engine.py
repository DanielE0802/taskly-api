# utils/template_engine.py
from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')))

def render_template(filename: str, context: dict) -> str:
    template = env.get_template(filename)
    return template.render(**context)