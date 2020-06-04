# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from reddash.app import app, update_variables
from reddash.app.home import blueprint
from flask import render_template, redirect, url_for, session, request, jsonify, Response
from jinja2 import TemplateNotFound
import websocket
import json
import time
import random
import logging
import datetime

dashlog = logging.getLogger("reddash")

def update_core():
    while True:
        time.sleep(0.5)
        try:
            yield f"data: {app.variables['servers']}, {app.variables['users']}, {app.variables['onlineusers']}\n\n"
        except KeyError:
            yield ""

# --------------------------------------- API ---------------------------------------

@blueprint.route('/api/stream')
def stream():
    return Response(update_core(), mimetype="text/event-stream")

@blueprint.route('/api/getservers')
def getservers():
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})
    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC__GET_USERS_SERVERS",
            "params": [int(session['id'])]
        }
        with app.lock:
            app.ws.send(json.dumps(requeststr))
            result = json.loads(app.ws.recv())
            if 'error' in result:
                if result['error']['message'] == "Method not found":
                    return jsonify({"status": 0, "message": "Not connected to bot"})
                dashlog.error(result['error'])
                return jsonify({"status": 0, "message": "Something went wrong"})
            if isinstance(result['result'], dict) and result['result'].get("disconnected", False):
                return jsonify({"status": 0, "message": "Not connected to bot"})
            return jsonify({"status": 1, "data": result['result']})
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})

@blueprint.route('/api/serverprefix', methods=['POST'])
def serverprefix():
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (end := app.cooldowns["serverprefix"].get(session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5))) > datetime.datetime.now():
        return jsonify({"status": 0, "message": f"You are doing that too much.  Try again in {(end - datetime.datetime.now()).seconds} seconds"})
    app.cooldowns["serverprefix"][session.get("id")] = datetime.datetime.now() + datetime.timedelta(seconds=5)

    data = request.json
    guildid = data.get("guild")
    userid = session.get("id")
    method = "set"
    prefixes = data.get("prefixes")
    if not (guildid and prefixes):
        return jsonify({"status": 0, "message": "Guild ID and prefixes must be specified"})
    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_BOTSETTINGS__SERVERPREFIX",
            "params": [int(guildid), int(userid), method, prefixes]
        }
        with app.lock:
            app.ws.send(json.dumps(requeststr))
            result = json.loads(app.ws.recv())
            if 'error' in result:
                if result['error']['message'] == "Method not found":
                    return jsonify({"status": 0, "message": "Not connected to bot"})
                dashlog.error(result['error'])
                return jsonify({"status": 0, "message": "Something went wrong"})
            if isinstance(result['result'], dict) and result['result'].get("disconnected", False):
                return jsonify({"status": 0, "message": "Not connected to bot"})
            return jsonify({"status": 1, "data": result['result']})
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})

@blueprint.route('/api/adminroles', methods=['POST'])
def adminroles():
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (end := app.cooldowns["adminroles"].get(session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5))) > datetime.datetime.now():
        return jsonify({"status": 0, "message": f"You are doing that too much.  Try again in {(end - datetime.datetime.now()).seconds} seconds"})
    app.cooldowns["adminroles"][session.get("id")] = datetime.datetime.now() + datetime.timedelta(seconds=5)

    data = request.json
    guildid = data.get("guild")
    userid = session.get("id")
    method = "set"
    roles = data.get("roles")
    if not guildid:
        return jsonify({"status": 0, "message": "Guild ID must be specified"})
    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_BOTSETTINGS__ADMINROLES",
            "params": [int(guildid), int(userid), method, roles]
        }
        with app.lock:
            app.ws.send(json.dumps(requeststr))
            result = json.loads(app.ws.recv())
            if 'error' in result:
                if result['error']['message'] == "Method not found":
                    return jsonify({"status": 0, "message": "Not connected to bot"})
                dashlog.error(result['error'])
                return jsonify({"status": 0, "message": "Something went wrong"})
            if isinstance(result['result'], dict) and result['result'].get("disconnected", False):
                return jsonify({"status": 0, "message": "Not connected to bot"})
            return jsonify({"status": 1, "data": result['result']})
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})

@blueprint.route('/api/modroles', methods=['POST'])
def modroles():
    if not session.get("id"):
        return jsonify({"status": 0, "message": "Not logged in"})

    if (end := app.cooldowns["modroles"].get(session.get("id"), datetime.datetime.now() - datetime.timedelta(seconds=5))) > datetime.datetime.now():
        return jsonify({"status": 0, "message": f"You are doing that too much.  Try again in {(end - datetime.datetime.now()).seconds} seconds"})
    app.cooldowns["modroles"][session.get("id")] = datetime.datetime.now() + datetime.timedelta(seconds=5)

    data = request.json
    guildid = data.get("guild")
    userid = session.get("id")
    method = "set"
    roles = data.get("roles")
    if not guildid:
        return jsonify({"status": 0, "message": "Guild ID must be specified"})
    try:
        requeststr = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "DASHBOARDRPC_BOTSETTINGS__MODROLES",
            "params": [int(guildid), int(userid), method, roles]
        }
        with app.lock:
            app.ws.send(json.dumps(requeststr))
            result = json.loads(app.ws.recv())
            if 'error' in result:
                if result['error']['message'] == "Method not found":
                    return jsonify({"status": 0, "message": "Not connected to bot"})
                dashlog.error(result['error'])
                return jsonify({"status": 0, "message": "Something went wrong"})
            if isinstance(result['result'], dict) and result['result'].get("disconnected", False):
                return jsonify({"status": 0, "message": "Not connected to bot"})
            return jsonify({"status": 1, "data": result['result']})
    except:
        return jsonify({"status": 0, "message": "Not connected to bot"})

# --------------------------------------- API ---------------------------------------

# -------------------------------------- Routes -------------------------------------

@blueprint.route('/')
def root():
    return redirect('/')

@blueprint.route('/index')
def index():
    return render_template('index.html')

@blueprint.route('/commands')
def commands():    
    data = app.commanddata
    prefix = app.variables.get("prefix", ["[p]"])

    return render_template("commands.html", cogs=[k['name'] for k in data], data=data, prefixes=prefix)

@blueprint.route('/credits')
def credits():
    return render_template("credits.html")

@blueprint.route('/guild/<int:guild>')
def guild(guild):
    if not session.get("id"):
        return redirect(url_for('base_blueprint.login'))
    # We won't disconnect the websocket here, even if it fails, so that the main updating thread doesnt run into issues
    try:
        request = {
            "jsonrpc": "2.0",
            "id": random.randint(1, 1000),
            "method": "DASHBOARDRPC__GET_SERVER",
            "params": [int(session['id']), int(guild)]
        }
        with app.lock:
            app.ws.send(json.dumps(request))
            result = json.loads(app.ws.recv())
            data = {}
            if 'error' in result:
                if result['error']['message'] == "Method not found":
                    data = {"status": 0, "message": "Not connected to bot"}
                else:
                    dashlog.error(result['error'])
                    data = {"status": 0, "message": "Something went wrong"}
            if isinstance(result['result'], dict) and result['result'].get("disconnected", False):
                data = {"status": 0, "message": "Not connected to bot"}
        if not data:
            data = {"status": 1, "data": result['result']}
    except:
        data = {"status": 0, "message": "Not connected to bot"}
    return render_template("guild.html", data=data)

@blueprint.route('/<template>')
def route_template(template):

    if not session.get("id"):
        return redirect(url_for('base_blueprint.login'))

    try:

        return render_template(template + '.html')

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500
