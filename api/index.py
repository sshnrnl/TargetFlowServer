from os.path import dirname, basename, isfile, join
import glob
from flask import Flask, render_template, request, redirect, url_for, make_response, session, jsonify, Response # type: ignore
from flask_cors import CORS, cross_origin # type: ignore
import os
from dotenv import load_dotenv # type: ignore
from flask_sqlalchemy import SQLAlchemy# type: ignore
from hori import *
import jwt # type: ignore
import pymysql# type: ignore
from flask_migrate import Migrate

pymysql.install_as_MySQLdb()

load_dotenv()

app = Flask(__name__, static_folder=os.getcwd().replace('\\', "\\\\") + '/assets', template_folder='../pages', static_url_path='/assets')
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Load MySQL URL from .env
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
}

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app, resources={r'*': {'origin': ['*']}}, supports_credentials=True)

route = glob.glob(join(dirname(__file__) ,"*.py"))
__all__ = [ basename(f)[:-3] for f in route if isfile(f) and not f.endswith('__init__.py')]
for j in __all__:
    __import__(f'api.'+j)
