# app/utils/template_engine.py
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
