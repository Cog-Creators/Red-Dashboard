# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from reddash.app import app
from reddash.app.home import blueprint
from flask import render_template, redirect, url_for, session, request, jsonify, Response, g
from flask_babel import _, refresh
from jinja2 import TemplateNotFound
import websocket
import json
import time
import random
import logging
import datetime

dashlog = logging.getLogger("reddash")


def get_result(app, requeststr):
    app.ws.send(json.dumps(requeststr))
    result = json.loads(app.ws.recv())
    if "error" in result:
        if result["error"]["message"] == "Method not found":
            return jsonify({"status": 0, "message": _("Not connected to bot")})
        dashlog.error(result["error"])
        return jsonify({"status": 0, "message": _("Something went wrong")})
    if isinstance(result["result"], dict) and result["result"].get("disconnected", False):
        return jsonify({"status": 0, "message": _("Not connected to bot")})
    return jsonify({"status": 1, "data": result["result"]})


# --------------------------------------- API ---------------------------------------


@blueprint.route("/api/getservers")
def getservers():
    if not session.get("id"):
        return jsonify({"status": 0, "message": _("Not logged in")})
    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC__GET_USERS_SERVERS",
            "params": [str(g.id)],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": _("Not connected to bot")})


@blueprint.route("/api/<guild>/serverprefix", methods=["POST"])
def serverprefix(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": _("Not logged in")})

    if (
        end := app.cooldowns["serverprefix"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["serverprefix"][
        session.get("id")
    ] = datetime.datetime.now() + datetime.timedelta(seconds=5)

    data = request.json
    userid = g.id
    method = "set"
    prefixes = data.get("prefixes")

    if not prefixes:
        return jsonify({"status": 0, "message": _("Prefixes must be specified")})

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_BOTSETTINGS__SERVERPREFIX",
            "params": [str(guild), str(userid), method, prefixes],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/api/<guild>/adminroles", methods=["POST"])
def adminroles(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (
        end := app.cooldowns["adminroles"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["adminroles"][session.get("id")] = datetime.datetime.now() + datetime.timedelta(
        seconds=5
    )

    data = request.json
    userid = g.id
    method = "set"
    roles = data.get("roles")

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_BOTSETTINGS__ADMINROLES",
            "params": [str(guild), str(userid), method, roles],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/api/<guild>/modroles", methods=["POST"])
def modroles(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (
        end := app.cooldowns["modroles"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["modroles"][session.get("id")] = datetime.datetime.now() + datetime.timedelta(
        seconds=5
    )

    data = request.json
    userid = g.id
    method = "set"
    roles = data.get("roles")

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_BOTSETTINGS__MODROLES",
            "params": [str(guild), str(userid), method, roles],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/api/<guild>/fetchrules", methods=["GET"])
def fetchrules(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (
        end := app.cooldowns["fetchrules"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["fetchrules"][session.get("id")] = datetime.datetime.now() + datetime.timedelta(
        seconds=5
    )

    userid = g.id

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_PERMISSIONS__FETCH_GUILD_RULES",
            "params": [str(guild), str(userid)],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/api/<guild>/fetchtargets", methods=["GET"])
def fetchtargets(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (
        end := app.cooldowns["fetchtargets"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=10)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["fetchtargets"][
        session.get("id")
    ] = datetime.datetime.now() + datetime.timedelta(seconds=10)

    userid = g.id

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_PERMISSIONS__FETCH_GUILD_TARGETS",
            "params": [str(guild), str(userid)],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/api/<guild>/fetchcogcommands", methods=["GET"])
def fetchcogcommands(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (
        end := app.cooldowns["fetchcogcommands"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["fetchcogcommands"][
        session.get("id")
    ] = datetime.datetime.now() + datetime.timedelta(seconds=5)

    userid = g.id

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_PERMISSIONS__FETCH_COG_COMMANDS",
            "params": [str(guild), str(userid)],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/api/<guild>/addrule", methods=["POST"])
def addrule(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (
        end := app.cooldowns["addrule"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["addrule"][session.get("id")] = datetime.datetime.now() + datetime.timedelta(
        seconds=5
    )

    data = request.json

    userid = g.id
    allow_or_deny = data.get("ad")
    who_or_what = data.get("ww")
    cog_or_command = data.get("cc")

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_PERMISSIONS__ADD_RULE",
            "params": [str(guild), str(userid), allow_or_deny, str(who_or_what), cog_or_command],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/api/<guild>/adddefaultrule", methods=["POST"])
def adddefaultrule(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (
        end := app.cooldowns["adddefaultrule"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["adddefaultrule"][
        session.get("id")
    ] = datetime.datetime.now() + datetime.timedelta(seconds=5)

    data = request.json

    userid = g.id
    allow_or_deny = data.get("ad")
    cog_or_command = data.get("cc")

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_PERMISSIONS__ADD_DEFAULT_RULE",
            "params": [str(guild), str(userid), allow_or_deny, cog_or_command],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/api/<guild>/removerule", methods=["POST"])
def removerule(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (
        end := app.cooldowns["removerule"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["removerule"][session.get("id")] = datetime.datetime.now() + datetime.timedelta(
        seconds=5
    )

    data = request.json

    userid = g.id
    who_or_what = data.get("ww")
    cog_or_command = data.get("cc")

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_PERMISSIONS__REMOVE_RULE",
            "params": [str(guild), str(userid), str(who_or_what), cog_or_command],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/api/<guild>/removedefaultrule", methods=["POST"])
def removedefaultrule(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (
        end := app.cooldowns["removedefaultrule"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["removedefaultrule"][
        session.get("id")
    ] = datetime.datetime.now() + datetime.timedelta(seconds=5)

    data = request.json

    userid = g.id
    cog_or_command = data.get("cc")

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_PERMISSIONS__REMOVE_DEFAULT_RULE",
            "params": [str(guild), str(userid), cog_or_command],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/api/<guild>/fetchaliases", methods=["GET"])
def fetchaliases(guild):
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (
        end := app.cooldowns["fetchaliases"].get(
            session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5)
        )
    ) > datetime.datetime.now():
        return jsonify(
            {
                "status": 0,
                "message": _("You are doing that too much.  Try again in {wait} seconds").format(
                    wait=(end - datetime.datetime.now()).seconds
                ),
            }
        )
    app.cooldowns["fetchaliases"][
        session.get("id")
    ] = datetime.datetime.now() + datetime.timedelta(seconds=5)

    userid = g.id

    try:
        int(guild)
    except ValueError:
        raise ValueError("Guild ID must be integer")

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_ALIASCC__FETCH_ALIASES",
            "params": [str(guild), str(userid)],
        }
        with app.lock:
            return get_result(app, requeststr)
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})


# --------------------------------------- API ---------------------------------------

# -------------------------------------- Routes -------------------------------------


@blueprint.route("/index")
@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/commands")
def commands():
    data = app.commanddata
    prefix = app.variables.get("prefix", ["[p]"])

    return render_template(
        "commands.html", cogs=[k["name"] for k in data], data=data, prefixes=prefix
    )


@blueprint.route("/credits")
def credits():
    return render_template("credits.html")


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
