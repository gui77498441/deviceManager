from flask import Blueprint
web = Blueprint('web',__name__)
from app.web import common


from app.web import adminView
from app.web import commonuserView