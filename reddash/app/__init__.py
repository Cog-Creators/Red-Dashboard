# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from flask import Flask, url_for, session, render_template
#from flask_session import Session
from importlib import import_module
from os import path
from cryptography import fernet
from io import StringIO
import base64
import threading
import time
import websocket
import traceback
import json
import sys
import os


class Lock:
    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, *args):
        self.lock.release()

global __version__
__version__ = "0.1.2a"
__author__ = "Neuro Assassin#4779"

# In case the dashboard cog isn't loaded
global defaults
defaults = {
    'botname': 'Red Discord Bot',
    'botavatar': 'https://cdn.discordapp.com/icons/133049272517001216/a_aab012f3206eb514cac0432182e9e9ec.gif?size=1024',
    'botinfo': 'Hello, welcome to the Red Discord Bot dashboard!  Here you can see basic information, commands list and even interact with your bot!  Unfortunately, this dashboard is not connected to any bot currently, so none of these features are available.  If you are the owner of the bot, please load the dashboard cog from Toxic Cogs.',
    'owner': 'Cog Creators'
}

global url
url = "ws://localhost:"

global app
app = None

global lock
lock = Lock()

def update_variables(method):
    try:
        while True:
            global app
            # Different wait times based on method, commands should be called less due to how much data it is
            if method == "DASHBOARDRPC__GET_VARIABLES":
                _id = 1
                time.sleep(app.interval)
            else:
                _id = 2
                time.sleep(app.interval * 2)

            request = {
                "jsonrpc": "2.0",
                "id": _id,
                "method": method,
                "params": []
            }
            with app.lock:
                # This needs to be inside the lock, or both threads will create a websocket
                if not app.ws:
                    app.ws = websocket.WebSocket()
                    try:
                        app.ws.connect(url)
                    except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException):
                        app.ws.close()
                        app.ws = None
                        continue
                try:
                    app.ws.send(json.dumps(request))
                except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException):
                    print("Connection reset")
                    app.ws.close()
                    app.ws = None
                    continue
                    
                try:
                    result = json.loads(app.ws.recv())
                except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException):
                    print("Connection reset")
                    app.ws.close()
                    app.ws = None
                    continue
                if 'error' in result:
                    if result['error']['message'] == "Method not found":
                        if method == "DASHBOARDRPC__GET_VARIABLES":
                            app.variables = {}
                        app.ws.close()
                        app.ws = None
                        continue
                    print(result['error'])
                    app.ws.close()
                    app.ws = None
                    continue
                if isinstance(result['result'], dict) and result['result'].get("disconnected", False):
                    # Dashboard cog unloaded, disconnect
                    if method == "DASHBOARDRPC__GET_VARIABLES":
                        app.variables = {}
                    app.ws.close()
                    app.ws = None
                    continue
            if method == "DASHBOARDRPC__GET_VARIABLES":
                app.variables = result['result']
            else:
                app.commanddata = result['result']
            app.variables["disconnected"] = False
    except Exception as e:
        print("".join(traceback.format_exception(type(e), e, e.__traceback__)))

def update_version():
    try:
        while True:
            time.sleep(1)
            if app.ws and app.ws.connected:
                request = {
                    "jsonrpc": "2.0",
                    "id": 0,
                    "method": "DASHBOARDRPC__CHECK_VERSION",
                    "params": [app.rpcversion]
                }
                with app.lock:
                    try:
                        app.ws.send(json.dumps(request))
                    except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException):
                        continue
                        
                    try:
                        result = json.loads(app.ws.recv())
                    except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException):
                        continue

                    if 'error' in result:
                        continue

                    if "disconnected" in result['result']:
                        continue

                    if result['result']['v'] != app.rpcversion and app.rpcversion != 0:
                        print("RPC webscocket behind.  Ignore upcoming socket closed messages.  Closing and restarting...")
                        app.ws.close()
                        app.ws = websocket.WebSocket()
                        app.ws.connect(url)
                    app.rpcversion = result['result']['v']
    except Exception as e:
        print("".join(traceback.format_exception(type(e), e, e.__traceback__)))

def register_blueprints(app):
    for module_name in ('base', 'home'):
        module = import_module('reddash.app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('page-404.html'), 404

def apply_themes(app):
    """
    Add support for themes.

    If DEFAULT_THEME is set then all calls to
      url_for('static', filename='')
      will modfify the url to include the theme name

    The theme parameter can be set directly in url_for as well:
      ex. url_for('static', filename='', theme='')

    If the file cannot be found in the /static/<theme>/ location then
      the url will not be modified and the file is expected to be
      in the default /static/ location
    """
    @app.context_processor
    def override_url_for():
        return dict(url_for=_generate_url_for_theme)

    def _generate_url_for_theme(endpoint, **values):
        if endpoint.endswith('static'):
            themename = values.get('theme', None) or \
                app.config.get('DEFAULT_THEME', None)
            if themename:
                theme_file = "{}/{}".format(themename, values.get('filename', ''))
                if path.isfile(path.join(app.static_folder, theme_file)):
                    values['filename'] = theme_file
        return url_for(endpoint, **values)

def add_constants(app):
    @app.context_processor
    def inject_variables():
        global __version__
        if not app.variables:
            return dict(version=__version__, **defaults)
        return dict(version=__version__, **app.variables)

def create_app(host, port, rpcport, interval, selenium=False):
    global url
    global app
    global lock

    url += str(rpcport)
    
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)

    app = Flask(__name__, static_folder='base/static')
    app.ws = None
    app.lock = lock
    app.variables = {}
    app.commanddata = {}
    app.config.from_object(__name__)
    app.secret_key = secret_key
    app.rpcport = str(rpcport)
    app.rpcversion = 0
    app.interval = interval
    
    if selenium:
        app.config['LOGIN_DISABLED'] = True
    register_blueprints(app)
    apply_themes(app)
    add_constants(app)
    
    vt = threading.Thread(target=update_variables, args=["DASHBOARDRPC__GET_VARIABLES"], daemon=True)
    vt.start()
    ct = threading.Thread(target=update_variables, args=["DASHBOARDRPC__GET_COMMANDS"], daemon=True)
    ct.start()
    pt = threading.Thread(target=update_version, daemon=True)
    pt.start()

    app.run(host=host, port=port)