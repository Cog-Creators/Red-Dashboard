from typing import Optional, SupportsInt
from importlib import import_module
from copy import deepcopy
from os import path
import datetime
import time
import json
import websocket
import jwt
import threading
import logging

from flask import render_template, redirect, request, url_for, session, g
from flask_babel import _
from rich import rule, columns, table as rtable, panel, text
from fuzzywuzzy import process

from reddash import __version__

from .constants import AVAILABLE_COLORS

WS_EXCEPTIONS = (
    ConnectionRefusedError,
    websocket._exceptions.WebSocketConnectionClosedException,
    ConnectionResetError,
    ConnectionAbortedError,
)


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
        if ip not in app.data.core["variables"]["oauth"]["blacklisted"]:
            g.id = get_user_id(app, request, session)
            if g.id is False and "id" in session:
                del session["id"]
                del session["avatar"]
                del session["username"]
        if ip in app.data.core["variables"]["oauth"]["blacklisted"]:
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
        variables = deepcopy(app.data.core["variables"])
        variables["locales"] = app.config["LOCALE_DICT"]
        variables["safelocales"] = json.dumps(app.config["LOCALE_DICT"])
        variables["selectedlocale"] = session.get("lang_code")
        variables["color"] = request.cookies.get("color", app.data.ui["default_color"])
        variables["sidebar"] = process_sidebar(app)
        variables["connected"] = app.config["RPC_CONNECTED"]
        variables["available_colors"] = AVAILABLE_COLORS
        variables = process_meta_tags(app, variables)

        return dict(version=__version__, variables=variables)


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
                # User had lang_code argument, and it closely matched a registered locale
                locale = processed[0]

        if not lang:
            # User either didn't have lang_code argument or wasnt able to match a locale
            # Let's check if theres something in the session
            lang = session.get("lang_code")
            if lang:
                # User has a locale in session
                locale = lang
            else:
                # User doesn't have lang_code, and doesn't have a locale stored in session.
                # Let's get the best one according to Flask
                locale = request.accept_languages.best_match(app.config["LANGUAGES"])

        # Let's save that so it will be used on next request as well
        session["lang_code"] = locale

    @babel.localeselector
    def get_locale():
        if not session.get("lang_code", None):
            session["lang_code"] = request.accept_languages.best_match(app.config["LANGUAGES"])
        return session["lang_code"]


def get_user_id(app, req, ses):
    try:
        payload = jwt.decode(ses["id"], app.jwt_secret_key, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, KeyError):
        return False
    except (jwt.InvalidSignatureError, jwt.InvalidTokenError):
        ip = req.environ.get("HTTP_X_FORWARDED_FOR") or req.remote_addr
        app.blacklisted.append(ip)
        thread = threading.Thread(target=notify_owner_of_blacklist, args=[app, ip])
        thread.start()
        return None
    return payload["userid"]


def process_meta_tags(app, variables):
    variables["meta"] = app.data.ui["meta"]

    if variables["meta"]["title"] == "":
        variables["meta"]["title"] = _("{name} Dashboard").format(name=variables["bot"]["name"])
    else:
        variables["meta"]["title"] = variables["meta"]["title"].replace(
            "{name}", variables["bot"]["name"]
        )

    if variables["meta"]["icon"] == "":
        variables["meta"]["icon"] = variables["bot"]["avatar"]

    if variables["meta"]["description"] == "":
        variables["meta"]["description"] = _(
            "Interactive dashboard to control and interact with {name}"
        ).format(name=variables["bot"]["name"])
    else:
        variables["meta"]["description"] = variables["meta"]["description"].replace(
            "{name}", variables["bot"]["name"]
        )

    if variables["meta"]["color"] == "":
        variables["meta"]["color"] = "#ff7575"

    return variables


def process_sidebar(app):
    logged_in = "id" in session
    sidebar = sorted(app.data.ui["sidebar"], key=lambda x: x["pos"])
    final = []

    initial_route = "/" + request.path.split("/")[1]

    for item in sidebar:
        item = {k: v for k, v in item.items()}
        if item["session"] is True and not logged_in:
            continue
        if item["session"] is False and logged_in:
            continue

        try:
            if item["admin"] and not (
                logged_in and str(g.id) in app.data.core["variables"]["bot"]["owners"]
            ):
                continue
        except AttributeError:
            # Not sure how this happens. Meh
            continue

        # I have to localize here opposed to storing it because... well... then it's not localized
        if item["name"] == "builtin-home":
            item["name"] = _("Home")
        elif item["name"] == "builtin-commands":
            item["name"] = _("Commands")
        elif item["name"] == "builtin-dashboard":
            item["name"] = _("Dashboard")
        elif item["name"] == "builtin-third_parties":
            item["name"] = _("Third Parties")
        elif item["name"] == "builtin-credits":
            item["name"] = _("Credits")
        elif item["name"] == "builtin-login":
            item["name"] = _("Login")
        elif item["name"] == "builtin-logout":
            item["name"] = _("Logout")
        elif item["name"] == "builtin-admin":
            item["name"] = _("Admin")

        if not item["is_http"]:
            item["route"] = url_for(item["route"])

        item["active"] = False
        if initial_route == item["route"] or (
            initial_route == "/guild" and item["route"] == "/dashboard"
        ):
            item["active"] = True

        final.append(item)

    return final


def startup_message(app, kwargs):
    table = rtable.Table(title="Settings")
    table.add_column("Setting", style="red", no_wrap=True)
    table.add_column("Value", style="blue", no_wrap=True)

    table.add_row("Version", __version__)
    table.add_row("Host", kwargs["host"])
    table.add_row("Webserver port", str(kwargs["port"]))
    table.add_row("RPC Port", str(app.config["WEBSOCKET_PORT"]))
    table.add_row("Update interval", str(app.config["WEBSOCKET_INTERVAL"]))
    table.add_row("Environment", "Development" if kwargs["dev"] else "Production")
    table.add_row("Logging level", "Debug" if kwargs["debug"] else "Warning")

    app.console.print(rule.Rule("Red Discord Bot Dashboard - Webserver"))

    disclaimer = text.Text(
        "The Red-Dashboard is in alpha development and not encouraged for public/official use. "
        "By running this program, you understand that potential harm may come to your data and "
        "corrupt your Redbot.",
        no_wrap=False,
    )

    app.console.print(
        columns.Columns([panel.Panel(table, expand=False), panel.Panel(disclaimer)], expand=True)
    )


def initialize_websocket(app):
    app.ws = websocket.WebSocket()
    try:
        app.ws.connect(f"ws://{app.config['WEBSOCKET_HOST']}:{app.config['WEBSOCKET_PORT']}")
    except WS_EXCEPTIONS:
        app.ws.close()
        app.ws = None
        return False
    return True


def secure_send(app, request):
    dashlog = logging.getLogger("reddash")
    try:
        app.ws.send(json.dumps(request))
    except WS_EXCEPTIONS:
        dashlog.warning("Connection reset")
        app.ws.close()
        app.ws = None
        return False

    try:
        result = json.loads(app.ws.recv())
    except WS_EXCEPTIONS:
        dashlog.warning("Connection reset")
        app.ws.close()
        app.ws = None
        return False
    else:
        return result


def check_for_disconnect(app, method, result):
    if "error" in result:
        if result["error"]["message"] == "Method not found":
            if method == "DASHBOARDRPC__GET_VARIABLES":
                app.config["RPC_CONNECTED"] = False
        else:
            dashlog = logging.getLogger("reddash")
            dashlog.error(result["error"])
        app.ws.close()
        app.ws = None
        return False
    if isinstance(result["result"], dict) and result["result"].get("disconnected", False):
        # Dashboard cog unloaded, disconnect
        app.config["RPC_CONNECTED"] = False
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


# This is taken from Red Discord Bot's chat_formatting.py
def humanize_timedelta(
    *, timedelta: Optional[datetime.timedelta] = None, seconds: Optional[SupportsInt] = None
) -> str:
    """
    Get a locale aware human timedelta representation.
    This works with either a timedelta object or a number of seconds.
    Fractional values will be omitted, and values less than 1 second
    an empty string.
    Parameters
    ----------
    timedelta: Optional[datetime.timedelta]
        A timedelta object
    seconds: Optional[SupportsInt]
        A number of seconds
    Returns
    -------
    str
        A locale aware representation of the timedelta or seconds.
    Raises
    ------
    ValueError
        The function was called with neither a number of seconds nor a timedelta object
    """

    try:
        obj = seconds if seconds is not None else timedelta.total_seconds()
    except AttributeError:
        raise ValueError("You must provide either a timedelta or a number of seconds")

    seconds = int(obj)
    periods = [
        (_("year"), _("years"), 60 * 60 * 24 * 365),
        (_("month"), _("months"), 60 * 60 * 24 * 30),
        (_("day"), _("days"), 60 * 60 * 24),
        (_("hour"), _("hours"), 60 * 60),
        (_("minute"), _("minutes"), 60),
        (_("second"), _("seconds"), 1),
    ]

    strings = []
    for period_name, plural_period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 0:
                continue
            unit = plural_period_name if period_value > 1 else period_name
            strings.append(f"{period_value} {unit}")

    return ", ".join(strings)
