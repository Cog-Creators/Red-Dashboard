# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for, session, g, make_response
from datetime import datetime, timedelta
from flask_babel import _, refresh

from reddash.app.base import blueprint
from reddash.app import app

import requests
import websocket
import json
import logging
import jwt

dashlog = logging.getLogger("reddash")


@blueprint.route("/error-<error>")
def route_errors(error):
    return render_template("errors/{}.html".format(error))


## Login & Registration


@blueprint.route("/callback", methods=["GET"])
def callback():
    try:
        code = request.args["code"]
    except KeyError:
        return render_template("login/login.html", status="1")
    requestobj = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "DASHBOARDRPC__GET_SECRET",
        "params": [],
    }
    if app.ws and app.ws.connected:
        with app.lock:
            try:
                app.ws.send(json.dumps(requestobj))
                result = json.loads(app.ws.recv())
            except (
                ConnectionRefusedError,
                websocket._exceptions.WebSocketConnectionClosedException,
                ConnectionResetError,
            ):
                return render_template("login/login.html", status="4")
            if "error" in result:
                if result["error"]["message"] == "Method not found":
                    return render_template("login/login.html", status="4")
                else:
                    dashlog.error(result["error"])
                    return render_template("login/login.html", status="5")
            if isinstance(result["result"], dict) and result["result"].get("disconnected", False):
                return render_template("login/login.html", status="4")
            secret = result["result"]["secret"]
    else:
        return render_template("login/login.html", status="4")
    redirectstr = app.variables["redirect"]
    data = {
        "client_id": int(app.variables["clientid"]),
        "client_secret": secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirectstr,
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
        return render_template("login/login.html", status="2")
    new = requests.get(
        "https://discordapp.com/api/v6/users/@me", headers={"Authorization": f"Bearer {token}"},
    )
    new_data = new.json()
    if "id" in new_data:
        payload = {
            "userid": new_data["id"],
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=30),
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
    return render_template("login/login.html", status="3")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if not session.get("id"):
        return render_template("login/login.html", status="0")
    return redirect(url_for("base_blueprint.index"))


@blueprint.route("/logout")
def logout():
    del session["id"]
    return redirect(url_for("base_blueprint.login"))


@blueprint.route("/blacklisted")
def blacklisted():
    return render_template("errors/blacklisted.html")


@blueprint.route("/setcolor", methods=["POST"])
def set_color():
    resp = make_response(jsonify({"status": 1}))
    resp.set_cookie("color", request.json.get("color"))
    return resp


@blueprint.route("/index")
@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/commands")
def commands():
    data = app.commanddata
    prefix = app.variables.get("prefix", ["[p]"])

    return render_template(
        "pages/commands.html", cogs=[k["name"] for k in data], data=data, prefixes=prefix
    )


@blueprint.route("/credits")
def credits():
    return render_template("pages/credits.html")


## Errors


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template("errors/403.html"), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500
