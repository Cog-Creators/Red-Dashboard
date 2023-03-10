# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import (
    jsonify,
    render_template,
    redirect,
    request,
    url_for,
    session,
    g,
    make_response,
    abort,
)
from datetime import datetime, timedelta

from reddash.app.utils import humanize_timedelta
from reddash.app.base import blueprint
from reddash.app import app

from copy import deepcopy
import requests
import logging
import random
import string
import jwt

dashlog = logging.getLogger("reddash")


@blueprint.route("/error-<error>")
def route_errors(error):
    return render_template("errors/{}.html".format(error))


# Login & Registration
@blueprint.route("/callback", methods=["GET"])
def callback():
    try:
        code = request.args["code"]
    except KeyError:
        return redirect(url_for("base_blueprint.login_error_auth_denied"))

    if "state" not in session or "state" not in request.args:
        return redirect(url_for("base_blueprint.login_error_missing_state"))

    if session["state"] != request.args["state"]:
        return redirect(url_for("base_blueprint.login_error_invalid_state"))

    del session["state"]

    data = {
        "client_id": int(app.data.core["variables"]["bot"]["clientid"]),
        "client_secret": app.data.core["variables"]["oauth"]["secret"],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": app.data.core["variables"]["oauth"]["redirect"],
        "scope": "identify",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        "https://discordapp.com/api/v6/oauth2/token", data=data, headers=headers
    )
    try:
        token = response.json()["access_token"]
    except KeyError:
        dashlog.error(f"Failed to log someone in.\n{response.json()}")
        return redirect(url_for("base_blueprint.login_error_invalid_config"))
    new = requests.get(
        "https://discordapp.com/api/v6/users/@me", headers={"Authorization": f"Bearer {token}"},
    )
    new_data = new.json()
    if "id" in new_data:
        payload = {
            "userid": new_data["id"],
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=60),
        }
        token = jwt.encode(payload, app.jwt_secret_key, algorithm="HS256")
        session["id"] = token
        session[
            "avatar"
        ] = f"https://cdn.discordapp.com/avatars/{new_data['id']}/{new_data['avatar']}.png"
        session["username"] = new_data["username"]

        redirecting_to = "base_blueprint.index"
        arguments = {}
        if session.get("login_redirect"):
            redirecting_to = session["login_redirect"]["route"]
            arguments = session["login_redirect"]["kwargs"]
            del session["login_redirect"]

        return redirect(url_for(redirecting_to, **arguments))
    dashlog.error(f"Failed to obtain a user's profile.\n{new.json()}")
    return redirect(url_for("base_blueprint.login_error_discord_error"))


@blueprint.route("/admin", methods=["GET"])
def admin():
    if not session.get("id"):
        return render_template("login/login.html", status="0")

    if not str(g.id) in app.data.core["variables"]["bot"]["owners"]:
        abort(403)

    uptime_str = humanize_timedelta(timedelta=datetime.utcnow() - app.config["LAUNCH"])
    connection_str = humanize_timedelta(timedelta=datetime.utcnow() - app.config["LAST_RPC_EVENT"])

    sidebar = sorted(deepcopy(app.data.ui["sidebar"]), key=lambda x: x["pos"])
    default_color = app.data.ui["default_color"]

    return render_template(
        "pages/admin.html",
        ws_uptime=uptime_str,
        connection_uptime=connection_str,
        editable_sidebar=sidebar,
        default_color=default_color,
    )


@blueprint.route("/login", methods=["GET"])
def login():
    if not session.get("id"):
        return render_template("login/login.html", status="0")
    return redirect(url_for("base_blueprint.index"))


@blueprint.route("/login/error/auth-denied", methods=["GET"])
def login_error_auth_denied():
    if not session.get("id"):
        return render_template("login/login.html", status="1")
    return redirect(url_for("base_blueprint.index"))


@blueprint.route("/login/error/invalid-config", methods=["GET"])
def login_error_invalid_config():
    if not session.get("id"):
        return render_template("login/login.html", status="2")
    return redirect(url_for("base_blueprint.index"))


@blueprint.route("/login/error/discord-error", methods=["GET"])
def login_error_discord_error():
    if not session.get("id"):
        return render_template("login/login.html", status="3")
    return redirect(url_for("base_blueprint.index"))


@blueprint.route("/login/error/missing-state", methods=["GET"])
def login_error_missing_state():
    if not session.get("id"):
        return render_template("login/login.html", status="4")
    return redirect(url_for("base_blueprint.index"))


@blueprint.route("/login/error/invalid-state", methods=["GET"])
def login_error_invalid_state():
    if not session.get("id"):
        return render_template("login/login.html", status="5")
    return redirect(url_for("base_blueprint.index"))


@blueprint.route("/login/discord", methods=["GET"])
def discord_oauth():
    state = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
    session["state"] = state

    return redirect(
        f"https://discordapp.com/api/oauth2/authorize?client_id={app.data.core['variables']['bot']['clientid']}&redirect_uri={app.data.core['variables']['oauth']['redirect']}&response_type=code&scope=identify&state={state}"
    )


@blueprint.route("/logout", methods=["GET"])
def logout():
    del session["id"]
    del session["avatar"]
    del session["username"]
    return redirect(url_for("base_blueprint.login"))


@blueprint.route("/blacklisted")
def blacklisted():
    return render_template("errors/blacklisted.html")


@blueprint.route("/setcolor", methods=["POST"])
def set_color():
    resp = make_response(jsonify({"status": 1}))
    resp.set_cookie(
        "color", request.json.get("color"), expires=datetime.now() + timedelta(days=365)
    )
    return resp


@blueprint.route("/index")
@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/commands")
def commands():
    data = app.data.core["commands"]
    prefix = app.data.core["variables"]["bot"]["prefix"]
    return render_template(
        "pages/commands.html", cogs=[k["name"] for k in data], data=data, prefixes=prefix
    )


@blueprint.route("/credits")
def credits():
    return render_template("pages/credits.html")


# Errors
@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template("errors/403.html"), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500
