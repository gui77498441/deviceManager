import os
from flask import Flask
from flask_mail import Mail

mail = Mail()

def create_app():
   
    # create and configure the app
    app = Flask(__name__)
    
    from app.web import web
    app.register_blueprint(web)

    return app