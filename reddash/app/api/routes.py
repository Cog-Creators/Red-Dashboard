from reddash.app import app
from reddash.app.api import blueprint
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

# ----------------------------------- Third Party -----------------------------------


@blueprint.route("/api/webhook", methods=("POST",))
def webhook_route():
    # Webhook received
    if not request.is_json:
        # reject any requests that aren't json for now
        return jsonify(
            {"status": 0, "message": "Invalid formatting. This endpoint receives JSON only."}
        )
    payload = request.get_json()
    payload["origin"] = request.origin
    payload["headers"] = str(request.headers)
    # Pass header data here incase there was something
    # else the user needs for filtering
    payload["user_agent"] = str(request.user_agent)
    # User agent seems adequate enough for filtering
    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_WEBHOOKS__WEBHOOK_RECEIVE",
            "params": [payload],
        }
        with app.lock:
            return get_result(app, requeststr)
    except Exception:
        dashlog.warning("Error sending webhook info", exc_info=True)
        return jsonify({"status": 0, "message": "Not connected to bot"})


@blueprint.route("/third_party/spotify/callback")
def third_party_spotify_callback():
    # Spotify cog is owned by TrustyJAID

    try:
        code = request.args["code"]
        state = request.args["state"]
    except KeyError:
        return render_template(
            "third_party/spotify.html",
            context="3",
            msg="You must authenticate using a link given by bot.",
        )

    if not session.get("id"):
        session["login_redirect"] = {
            "route": f"api_blueprint.third_party_spotify_callback",
            "kwargs": {"code": code, "state": state},
        }
        return redirect(url_for("base_blueprint.login"))

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_SPOTIFY__AUTHENTICATE_USER",
            "params": [str(g.id), code, state],
        }
        with app.lock:
            result = get_result(app, requeststr).json
        if result["status"] == 0:
            return render_template("third_party/spotify.html", context="2", msg=result["message"])
        if result["data"]["status"] == 0:
            return render_template(
                "third_party/spotify.html", context="3", msg=result["data"]["message"]
            )
        return render_template("third_party/spotify.html", context="1", msg="")
    except Exception as e:
        app.progress.print("".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return render_template("third_party/spotify.html", context="2", msg=str(e))
