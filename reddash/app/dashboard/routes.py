from reddash.app import app
from reddash.app.dashboard import blueprint
from flask import render_template, redirect, url_for, session, request, jsonify, Response, g
from flask_babel import _, refresh
from jinja2 import TemplateNotFound
import traceback
import websocket
import json
import time
import random
import logging
import datetime

dashlog = logging.getLogger("reddash")


@blueprint.route("/dashboard")
def dashboard():
    if not session.get("id"):
        return redirect(url_for("base_blueprint.login"))
    return render_template("dashboard.html")


@blueprint.route("/guild/<guild>")
def guild(guild):
    if not session.get("id"):
        return redirect(url_for("base_blueprint.login"))

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    # We won't disconnect the websocket here, even if it fails, so that the main updating thread doesnt run into issues
    try:
        request = {
            "jsonrpc": "2.0",
            "id": random.randint(1, 1000),
            "method": "DASHBOARDRPC__GET_SERVER",
            "params": [int(g.id), int(guild)],
        }
        with app.lock:
            app.ws.send(json.dumps(request))
            result = json.loads(app.ws.recv())
            data = {}
            if "error" in result:
                if result["error"]["message"] == "Method not found":
                    data = {"status": 0, "message": "Not connected to bot"}
                else:
                    dashlog.error(result["error"])
                    data = {"status": 0, "message": "Something went wrong"}
            if isinstance(result["result"], dict) and result["result"].get("disconnected", False):
                data = {"status": 0, "message": "Not connected to bot"}
        if not data:
            data = {"status": 1, "data": result["result"]}
    except:
        data = {"status": 0, "message": "Not connected to bot"}
    return render_template("guild.html", data=data)
