#############################################
#                                           #
#               Flask Module                #
#                                           #
#  Author: Shan                             #
#                                           #
#############################################

from flask import Flask, render_template, request, redirect, url_for, make_response,session,jsonify,Response
from flask_cors import CORS, cross_origin
import os
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room


app = Flask(__name__, static_folder=os.getcwd().replace('\\',"\\\\")+'/assets', template_folder='../pages',static_url_path='/assets')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)
CORS(app, resources={r'*':{'origin':['*']}}, supports_credentials=True)