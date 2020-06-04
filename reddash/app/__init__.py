# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from flask import Flask, url_for, session, render_template
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, TextColumn
from rich.columns import Columns
from rich.traceback import install, Trace, Traceback
from rich.rule import Rule
from rich.logging import RichHandler
from waitress import serve
from importlib import import_module
from os import path
from cryptography import fernet
from io import StringIO
import base64
import threading
import time
import websocket
import traceback
import logging
import rich
import json
import sys
import os

log = logging.getLogger('werkzeug')
dashlog = logging.getLogger('reddash')

console = Console()
oldexcepthook = install()
progress = Progress("{task.description}", TextColumn("{task.fields[status]}\n"))

logging.basicConfig(format="%(message)s", handlers=[RichHandler(console=progress)])

class Lock:
    def __init__(self):
        self.lock = threading.Lock()

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, *args):
        self.lock.release()

global __version__
__version__ = "0.1.3a"
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

global running
running = True

def update_variables(method, task):
    progress.update(task, status="[bold green]Running[/bold green]")
    progress.refresh()
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

            global running
            if not running:
                progress.update(task, status="[bold red]Killed[/bold red]")
                progress.refresh()
                return

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
                    except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException, ConnectionResetError):
                        app.ws.close()
                        app.ws = None
                        continue
                try:
                    app.ws.send(json.dumps(request))
                except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException, ConnectionResetError):
                    dashlog.warning("Connection reset")
                    app.ws.close()
                    app.ws = None
                    continue
                    
                try:
                    result = json.loads(app.ws.recv())
                except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException, ConnectionResetError):
                    dashlog.warning("Connection reset")
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
                    dashlog.error(result['error'])
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
        progress.update(task, status="[bold red]Stopped[/bold red]")
        progress.refresh()
        with console:
            if console.is_terminal:
                console.print(progress._live_render.position_cursor())
            console.print_exception()
            if console.is_terminal:
                console.print(progress._live_render)

def update_version(task):
    progress.update(task, status="[bold green]Running[/bold green]")
    progress.refresh()
    try:
        while True:
            time.sleep(1)
            global running
            if not running:
                progress.update(task, status="[bold red]Killed[/bold red]")
                progress.refresh()
                return
            if app.ws and app.ws.connected:
                request = {
                    "jsonrpc": "2.0",
                    "id": 0,
                    "method": "DASHBOARDRPC__CHECK_VERSION",
                    "params": [app.rpcversion]
                }
                with app.lock:
                    if not app.ws:
                        app.ws = websocket.WebSocket()
                        try:
                            app.ws.connect(url)
                        except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException, ConnectionResetError):
                            app.ws.close()
                            app.ws = None
                            continue

                    try:
                        app.ws.send(json.dumps(request))
                    except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException, ConnectionResetError):
                        continue
                        
                    try:
                        result = json.loads(app.ws.recv())
                    except (ConnectionRefusedError, websocket._exceptions.WebSocketConnectionClosedException, ConnectionResetError):
                        continue

                    if 'error' in result:
                        continue

                    if "disconnected" in result['result']:
                        continue

                    if result['result']['v'] != app.rpcversion and app.rpcversion != 0:
                        dashlog.warning("RPC websocket behind.  Closing and restarting...")
                        app.ws.close()
                        app.ws = websocket.WebSocket()
                        app.ws.connect(url)
                    app.rpcversion = result['result']['v']
    except Exception as e:
        progress.update(task, status="[bold red]Stopped[/bold red]")
        progress.refresh()
        with console:
            if console.is_terminal:
                console.print(progress._live_render.position_cursor())
            console.print_exception()
            if console.is_terminal:
                console.print(progress._live_render)

def check_if_connected(task):
    while True:
        global running
        if not running:
            app.ws.close()
            del app.ws
            progress.update(task, status="[bold red]Websocket Killed[/bold red]")
            progress.refresh()
            return
        time.sleep(0.1)
        if not (app.ws and app.ws.connected):
            progress.update(task, status="[bold red]Disconnected[/bold red]")
            progress.refresh()
        else:
            progress.update(task, status="[bold green]Connected[/bold green]")
            progress.refresh()

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

def create_app(host, port, rpcport, interval, debug, dev, selenium=False):
    global url
    global app
    global lock

    url += str(rpcport)
    
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)

    app = Flask('reddash', static_folder='app/base/static')
    app.ws = None
    app.lock = lock
    app.variables = {}
    app.commanddata = {}
    app.config.from_object(__name__)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.secret_key = secret_key
    app.rpcport = str(rpcport)
    app.rpcversion = 0
    app.interval = interval

    # Cooldowns (Yay!)
    app.cooldowns = {
        "serverprefix": {},
        "adminroles": {},
        "modroles": {}
    }
    
    if selenium:
        app.config['LOGIN_DISABLED'] = True
    register_blueprints(app)
    apply_themes(app)
    add_constants(app)

    if debug:
        log.setLevel(logging.DEBUG)
        dashlog.setLevel(logging.DEBUG)

    table = Table(title="Settings")
    table.add_column("Setting", style="red", no_wrap=True)
    table.add_column("Value", style="blue", no_wrap=True)

    table.add_row("Version", __version__)
    table.add_row("Host", host)
    table.add_row("Webserver port", str(port))
    table.add_row("RPC Port", str(rpcport))
    table.add_row("Update interval", str(interval))
    table.add_row("Environment", "Development" if dev else "Production")
    table.add_row("Logging level", "Debug" if debug else "Warning")

    progress.print(Rule("Red Discord Bot Dashboard - Webserver"))
    disclaimer = "This is an instance of Red Discord Bot Dashboard,\ncreated by Neuro Assassin. This package is\nprotected under an MIT License. Any action\nthat will breach this license (including but not\nlimited to, removal of credits) may result in a\nDMCA request, or possibly more.\n\n\n\nYou can view the license at\nhttps://github.com/NeuroAssassin/\nRed-Dashboard/blob/master/LICENSE."

    vartask = progress.add_task("Update variable task:", status="[bold blue]Starting[/bold blue]")
    cmdtask = progress.add_task("Update command task:", status="[bold blue]Starting[/bold blue]")
    vertask = progress.add_task("Update version task:", status="[bold blue]Starting[/bold blue]")
    contask = progress.add_task("RPC Connected", status="[bold blue]Starting[/bold blue]")

    progress.print(Columns([Panel(table), Panel(disclaimer)], equal=True))

    threads = []
    threads.append(threading.Thread(target=update_variables, args=["DASHBOARDRPC__GET_VARIABLES", vartask], daemon=True))
    threads.append(threading.Thread(target=update_variables, args=["DASHBOARDRPC__GET_COMMANDS", cmdtask], daemon=True))
    threads.append(threading.Thread(target=update_version, args=[vertask], daemon=True))
    threads.append(threading.Thread(target=check_if_connected, args=[contask], daemon=True))

    for t in threads:
        t.start()

    if dev:
        app.run(host=host, port=port, debug=debug)
    else:
        serve(app, host=host, port=port, _quiet=True)
    
    dashlog.fatal("Shutting down...")
    global running
    running = False
    for t in threads:
        t.join()
    
    dashlog.fatal("Webserver terminated")