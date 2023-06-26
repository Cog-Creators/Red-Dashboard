from reddash.app import app
from reddash.app.api import blueprint
from flask import (
    render_template,
    render_template_string,
    redirect,
    url_for,
    session,
    request,
    jsonify,
    g,
)
from flask_babel import _
import traceback
import json
import logging
import datetime

from pygments import highlight
from pygments.lexers import get_lexer_by_name, Python3TracebackLexer
from pygments.formatters import HtmlFormatter

from ..constants import AVAILABLE_COLORS
from ..utils import get_user_id

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

    page = request.args.get("page", 0)

    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC__GET_USERS_SERVERS",
            "params": [str(g.id), str(page)],
        }
        with app.lock:
            return get_result(app, requeststr)
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
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
    except Exception:
        return jsonify({"status": 0, "message": "Not connected to bot"})

# --------------------------------------- Admin ---------------------------------------

@blueprint.route("/api/setdefaultcolor", methods=["POST"])
def setdefaultcolor():
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if not str(g.id) in app.data.core["variables"]["bot"]["owners"]:
        return jsonify({"status": 0, "message": "Not bot owner"})

    data = request.json
    default_color = data["dc"].lower()
    for color in AVAILABLE_COLORS:
        if color["name"] == default_color or color["class"] == default_color:
            default_color = color["name"]
            break
    else:
        return jsonify({"status": 0, "message": "Color not found"})
    app.data.ui.update(default_color=default_color)

    return jsonify({"status": 2})


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


@blueprint.route(
    "/third_party/<cog_name>/<page>",
    methods=(
        "HEAD",
        "GET",
        "OPTIONS",
        "POST",
        "PATCH",
        "DELETE",
    ),
)
@blueprint.route(
    "/third_party/<cog_name>",
    methods=(
        "HEAD",
        "GET",
        "OPTIONS",
        "POST",
        "PATCH",
        "DELETE",
    ),
)
def third_party(cog_name, page=None):
    third_parties = app.data.core["variables"]["third_parties"]
    cog_name = cog_name.lower()
    if not cog_name or cog_name not in third_parties:
        return render_template(
            "errors/error_message.html",
            error_message="404: Looks like that third party doesn't exist... Strange...",
        )
    if page is not None:
        page = _page = page.lower()
    else:
        _page = "null"
    if _page not in third_parties[cog_name]:
        return render_template(
            "errors/error_message.html",
            error_message="404: Looks like that page doesn't exist... Strange...",
        )
    if request.method not in third_parties[cog_name][_page]["methods"]:
        return {"status": 1, "message": f"Method {request.method} not allowed."}
    context_ids = {}
    if "user_id" in third_parties[cog_name][_page]["context_ids"]:
        if not session.get("id"):
            session["login_redirect"] = {
                "route": "api_blueprint.third_party",
                "kwargs": {"cog_name": cog_name, "page": page, **request.args},
            }
            return redirect(url_for("base_blueprint.login"))
        else:
            context_ids["user_id"] = int(get_user_id(app=app, req=request, ses=session))
    if (
        "guild_id" in third_parties[cog_name][_page]["context_ids"]
        and "guild_id" not in request.args
    ):
        return render_template(
            "dashboard.html",
            base_guild_url=f"{request.path}?guild_id=123456789123456789"
            + (f"&{request.url.split('?')[-1]}" if len(request.url.split("?")) > 1 else ""),
        )
    kwargs = request.args.copy()
    for key in third_parties[cog_name][_page]["context_ids"]:
        if key == "user_id":
            continue
        try:
            context_ids[key] = int(kwargs[key])
        except KeyError:
            return render_template(
                "errors/error_message.html", error_message=f"Missing argument: `{key}`."
            )
        except ValueError:
            return render_template(
                "errors/error_message.html", error_message=f"Invalid argument: `{key}`."
            )
    for key in third_parties[cog_name][_page]["required_kwargs"]:
        if key not in kwargs:
            return render_template(
                "errors/error_message.html", error_message=f"Missing argument: `{key}`."
            )
    if request.method not in ["HEAD", "GET"] and request.json:
        kwargs["data"] = request.json
    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_THIRDPARTIES__DATA_RECEIVE",
            "params": [
                request.method,
                cog_name,
                page,
                context_ids,
                kwargs,
                session.get("lang_code", None),
            ],
        }
        with app.lock:
            result = get_result(app, requeststr).json
        if "data" in result:
            result = result["data"]
        if request.method not in ["HEAD", "GET"]:  # API request by JavaScript code or bot.
            return result
        if "web-content" in result:
            return render_template_string(result["web-content"], **result)
        elif "error_message" in result:
            return render_template(
                "errors/error_message.html", error_message=result["error_message"]
            )
        elif "redirect" in result:
            return render_template(result["redirect"], **result)
        return result
    except Exception as e:
        app.progress.print("".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return {"status": 1, "message": str(e)}


@app.template_filter("highlight")
def highlight_filter(code, language="python"):
    if language == "traceback":
        lexer = Python3TracebackLexer()
    else:
        lexer = get_lexer_by_name(language, stripall=True)
    formatter = HtmlFormatter()
    return highlight(code, lexer, formatter)
