from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'as23sdsf3243'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['UPLOAD_FOLDER'] = "C:/Users/Gio/Desktop/ecommerce/core/static/uploads"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from core.models import *
from core.routes import *
from core.api import *