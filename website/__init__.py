from flask import Flask, render_template, request, redirect, url_for, session
from .dbManager import dbManager
from flask_mail import Mail
from flask_cors import CORS
import website.parameters as parameters

dbManagerC = dbManager()
CORS_ALLOW_ORIGIN="*,*"
CORS_EXPOSE_HEADERS="*,*"
CORS_ALLOW_HEADERS="content-type,*"
app = Flask(__name__,template_folder='templates')
cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(",") , expose_headers= CORS_EXPOSE_HEADERS.split(","),   supports_credentials = True)
mail = Mail(app)

def create_app():
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
    app.config['MAIL_USERNAME'] = parameters.emailU
    app.config['MAIL_PASSWORD'] = parameters.emailP
    app.config['MAIL_DEFAULT_SENDER'] = parameters.emailU
    app.config["JSON_SORT_KEYS"] = False
    # mail settings
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] =  465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    from .routes import routes

    app.register_blueprint(routes, url_prefix='/')
    mail = Mail(app)
    
    return app