from importlib import import_module
from copy import copy
from os import path
import time
import json
import websocket

from flask import render_template, redirect, request, url_for, session
from rich import rule, columns, table as rtable, panel

from reddash.app.constants import DEFAULTS, WS_EXCEPTIONS, __version__


def register_blueprints(app):
    for module_name in ("base", "home"):
        module = import_module("reddash.app.{}.routes".format(module_name))
        app.register_blueprint(module.blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("page-404.html"), 404

    # This is so Babel automatically redirects to a proper locale
    @app.route("/")
    def home():
        session["lang_code"] = request.accept_languages.best_match(app.config["LANGUAGES"])
        return redirect(url_for("home_blueprint.index"))

    # This is so /callback automatically redirects to /<locale>/callback so it's not as confusing for owner to set the redirect
    @app.route("/callback")
    def redirect_callback():
        return redirect(url_for("base_blueprint.callback", **request.args))


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
        return dict(version=__version__, **variables)


def initialize_babel(app, babel):
    @babel.localeselector
    def get_locale():
        if not session.get("lang_code", None):
            session["lang_code"] = request.accept_languages.best_match(app.config["LANGUAGES"])
        return session["lang_code"]


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
    disclaimer = "This is an instance of Red Discord Bot Dashboard,\ncreated by Neuro Assassin. This package is\nprotected under the MIT License. Any action\nthat will breach this license (including but not\nlimited to, removal of credits) may result in a\nDMCA takedown request, or other legal\nconsequences.\n\n\n\nYou can view the license at\nhttps://github.com/NeuroAssassin/\nRed-Dashboard/blob/master/LICENSE."

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


def check_for_disconnect(app, result):
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
