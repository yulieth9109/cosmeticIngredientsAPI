from flask import Flask, render_template, request, redirect, url_for, session
from .dbManager import dbManager
from flask_cors import CORS
import website.parameters as parameters

dbManagerC = dbManager()
CORS_ALLOW_ORIGIN="*,*"
CORS_EXPOSE_HEADERS="*,*"
CORS_ALLOW_HEADERS="content-type,*"
app = Flask(__name__,template_folder='templates')
cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(",") , expose_headers= CORS_EXPOSE_HEADERS.split(","),   supports_credentials = True)

def create_app():
    app.config["JSON_SORT_KEYS"] = False
    from .routes import routes

    app.register_blueprint(routes, url_prefix='/')
    
    return app