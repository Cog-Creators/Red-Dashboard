# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import jsonify, render_template, redirect, request, url_for, session

from reddash.app.base import blueprint
from reddash.app import app
from reddash.app.base.util import verify_pass

import requests
import websocket
import json
import logging

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
        "client_id": int(app.variables["botid"]),
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
        session["id"] = new_data["id"]
        session[
            "avatar"
        ] = f"https://cdn.discordapp.com/avatars/{new_data['id']}/{new_data['avatar']}.png"
        session["username"] = new_data["username"]
        return redirect(url_for("home_blueprint.index"))
    dashlog.error(f"Failed to obtain a user's profile.\n{new.json()}")
    return render_template("login/login.html", status="3")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if not session.get("id"):
        return render_template("login/login.html", status="0")
    return redirect(url_for("home_blueprint.index"))


@blueprint.route("/logout")
def logout():
    del session["id"]
    return redirect(url_for("base_blueprint.login"))


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
