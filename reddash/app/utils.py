from importlib import import_module
from copy import copy
from os import path
import time
import json
import websocket
import jwt
import threading

from flask import render_template, redirect, request, url_for, session, g
from flask_babel import _
from rich import rule, columns, table as rtable, panel
from fuzzywuzzy import process

from reddash import __version__
from reddash.app.constants import DEFAULTS, WS_EXCEPTIONS


def register_blueprints(app):
    for module_name in ("base", "dashboard", "api"):
        module = import_module("reddash.app.{}.routes".format(module_name))
        app.register_blueprint(module.blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("page-404.html"), 404

    @app.before_request
    def blockip():
        ip = request.environ.get("HTTP_X_FORWARDED_FOR") or request.remote_addr
        if request.path.startswith(("/static", "/api/stream", "/blacklisted")):
            return
        if not ip in app.blacklisted:
            g.id = get_user_id(app, request, session)
            if g.id is False and "id" in session:
                del session["id"]
        if ip in app.blacklisted:
            return redirect(url_for("base_blueprint.blacklisted"))


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
        if endpoint.endswith("static"):
            themename = values.get("theme", None) or app.config.get("DEFAULT_THEME", None)
            if themename:
                theme_file = "{}/{}".format(themename, values.get("filename", ""))
                if path.isfile(path.join(app.static_folder, theme_file)):
                    values["filename"] = theme_file
            values["q"] = time.time()  # So Flask doesn't cache
        values["lang_code"] = session.get("lang_code", "en")
        return url_for(endpoint, **values)


def add_constants(app):
    @app.context_processor
    def inject_variables():
        variables = app.variables
        if not app.variables:
            variables = copy(DEFAULTS)
        variables["locales"] = app.config["LOCALE_DICT"]
        variables["safelocales"] = json.dumps(app.config["LOCALE_DICT"])
        variables["selectedlocale"] = session.get("lang_code")
        variables["color"] = request.cookies.get("color", variables["color"])
        variables["basepath"] = request.environ.get("HTTP_X_SCRIPT_NAME", "")
        variables = process_meta_tags(variables)
        return dict(version=__version__, **variables)


def initialize_babel(app, babel):
    @app.before_request
    def pull_locale():
        # Locale is determined in the following priority:
        #  lang_code argument
        #  lang_code session value
        #  default from browser
        args = request.args
        try:
            lang = args.get("lang_code", None)
        except AttributeError:
            lang = None

        if lang:
            # User had lang_code argument in request, lets check if its valid
            processed = process.extractOne(lang, app.config["LANGUAGES"])
            if processed[1] < 80:
                # Too low of a match, abort lang_code argument and go to session value
                lang = None
            else:
                # User had lang_code argument, and it closely matched a registered locale.  This will be used
                locale = processed[0]

        if not lang:
            # User either did not have lang_code argument or it wasnt able to match a registered locale.
            # Let's check if theres something in the session
            lang = session.get("lang_code")
            if lang:
                # User has a locale in session, that is already confirmed (otherwise would not be registered)
                locale = lang
            else:
                # User does not have lang_code argument, and does not have a locale stored in sesion.
                # Let's get the best one according to Flask
                locale = request.accept_languages.best_match(app.config["LANGUAGES"])

        # Locale variable is now the determined locale.  Let's save that so it will be used on next request as well
        session["lang_code"] = locale

    @babel.localeselector
    def get_locale():
        if not session.get("lang_code", None):
            session["lang_code"] = request.accept_languages.best_match(app.config["LANGUAGES"])
        return session["lang_code"]


def get_user_id(app, req, ses):
    try:
        payload = jwt.decode(ses["id"], app.jwt_secret_key, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, KeyError) as error:
        return False
    except (jwt.InvalidSignatureError, jwt.InvalidTokenError) as error:
        ip = req.environ.get("HTTP_X_FORWARDED_FOR") or req.remote_addr
        app.blacklisted.append(ip)
        thread = threading.Thread(target=notify_owner_of_blacklist, args=[app, ip])
        thread.start()
        return None
    return payload["userid"]


def process_meta_tags(variables):
    if "meta" not in variables:
        variables["meta"] = {"title": "", "icon": "", "description": "", "color": ""}

    if variables["meta"]["title"] == "":
        variables["meta"]["title"] = _("{name} Dashboard").format(name=variables["botname"])
    else:
        variables["meta"]["title"] = variables["meta"]["title"].replace(
            "{name}", variables["botname"]
        )

    if variables["meta"]["icon"] == "":
        variables["meta"]["icon"] = variables["botavatar"]

    if variables["meta"]["description"] == "":
        variables["meta"]["description"] = _(
            "Interactive dashboard to control and interact with {name}"
        ).format(name=variables["botname"])
    else:
        variables["meta"]["description"] = variables["meta"]["description"].replace(
            "{name}", variables["botname"]
        )

    if variables["meta"]["color"] == "":
        variables["meta"]["color"] = "#ff7575"

    return variables


def startup_message(app, progress, kwargs):
    table = rtable.Table(title="Settings")
    table.add_column("Setting", style="red", no_wrap=True)
    table.add_column("Value", style="blue", no_wrap=True)

    table.add_row("Version", __version__)
    table.add_row("Host", kwargs["host"])
    table.add_row("Webserver port", str(kwargs["port"]))
    table.add_row("RPC Port", str(app.rpcport))
    table.add_row("Update interval", str(app.interval))
    table.add_row("Environment", "Development" if kwargs["dev"] else "Production")
    table.add_row("Logging level", "Debug" if kwargs["debug"] else "Warning")

    progress.print(rule.Rule("Red Discord Bot Dashboard - Webserver"))
    disclaimer = "This is an instance of Red Discord Bot Dashboard,\ncreated by Neuro Assassin. This package is\nprotected under the AGPL License. Any action\nthat will breach this license (including but not\nlimited to, removal of credits) may result in a\nDMCA takedown request, or other legal\nconsequences.\n\n\nYou can view the license at\nhttps://github.com/Cog-Creators/\nRed-Dashboard/blob/master/LICENSE."

    vartask = progress.add_task("Update variable task:", status="[bold blue]Starting[/bold blue]")
    cmdtask = progress.add_task("Update command task:", status="[bold blue]Starting[/bold blue]")
    vertask = progress.add_task("Update version task:", status="[bold blue]Starting[/bold blue]")
    contask = progress.add_task("RPC Connected", status="[bold blue]Starting[/bold blue]")

    progress.print(columns.Columns([panel.Panel(table), panel.Panel(disclaimer)], equal=True))
    return {"var": vartask, "cmd": cmdtask, "ver": vertask, "con": contask}


def initialize_websocket(app):
    app.ws = websocket.WebSocket()
    try:
        app.ws.connect(app.ws_url)
    except WS_EXCEPTIONS:
        app.ws.close()
        app.ws = None
        return False
    return True


def secure_send(app, request):
    try:
        app.ws.send(json.dumps(request))
    except WS_EXCEPTIONS:
        app.dashlog.warning("Connection reset")
        app.ws.close()
        app.ws = None
        return False

    try:
        result = json.loads(app.ws.recv())
    except WS_EXCEPTIONS:
        app.dashlog.warning("Connection reset")
        app.ws.close()
        app.ws = None
        return False
    else:
        return result


def check_for_disconnect(app, method, result):
    if "error" in result:
        if result["error"]["message"] == "Method not found":
            if method == "DASHBOARDRPC__GET_VARIABLES":
                app.variables = {}
        else:
            app.dashlog.error(result["error"])
        app.ws.close()
        app.ws = None
        return False
    if isinstance(result["result"], dict) and result["result"].get("disconnected", False):
        # Dashboard cog unloaded, disconnect
        if method == "DASHBOARDRPC__GET_VARIABLES":
            app.variables = {}
        app.ws.close()
        app.ws = None
        return False
    return True


def notify_owner_of_blacklist(app, ip):
    while True:
        if app.ws and app.ws.connected:
            request = {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "DASHBOARDRPC__NOTIFY_OWNERS_OF_BLACKLIST",
                "params": [ip],
            }
            with app.lock:
                if not app.ws:
                    initialized = initialize_websocket(app)
                    if not initialized:
                        time.sleep(1)
                        continue

                result = secure_send(app, request)
                if not result or "error" in result:
                    time.sleep(1)
                    continue
                break
        time.sleep(1)


class ReverseProxied(object):
    def __init__(self, app, script_name=None, scheme=None, server=None):
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "") or self.script_name
        if script_name:
            environ["SCRIPT_NAME"] = script_name
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO"] = path_info[len(script_name) :]
        scheme = environ.get("HTTP_X_SCHEME", "") or self.scheme
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        server = environ.get("HTTP_X_FORWARDED_HOST", "") or self.server
        if server:
            environ["HTTP_HOST"] = server
        return self.app(environ, start_response)
