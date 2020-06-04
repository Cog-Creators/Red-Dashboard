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

@blueprint.route('/')
def route_default():
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/error-<error>')
def route_errors(error):
    return render_template('errors/{}.html'.format(error))

## Login & Registration

@blueprint.route('/callback', methods=['GET'])
def callback():
    try:
        code = request.args.get("code")
    except KeyError:
        return jsonify({"msg": "Missing code argument", "args": str(request.args)})
    redirectstr = app.variables['redirect']
    requestobj = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "DASHBOARDRPC__GET_SECRET",
        "params": []
    }
    with app.lock:
        app.ws.send(json.dumps(requestobj))
        result = json.loads(app.ws.recv())
        if 'error' in result:
            if result['error']['message'] == "Method not found":
                return jsonify({"msg": "Not connected to bot"})
            else:
                dashlog.error(result['error'])
                return jsonify({"msg": "Something went wrong"})
        if isinstance(result['result'], dict) and result['result'].get("disconnected", False):
            return jsonify({"msg": "Not connected to bot"})
        secret = result['result']['secret']
    data = {
        "client_id": int(app.variables['botid']),
        "client_secret": secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirectstr,
        "scope": "identify"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post("https://discordapp.com/api/v6/oauth2/token", data=data, headers=headers)
    try:
        token = response.json()["access_token"]
    except KeyError:
        dashlog.error(f"Failed to log someone in.\n{response.json()}")
        return jsonify({"msg": "Failed to obtain token", "returned": response.json()})
    new = requests.get("https://discordapp.com/api/v6/users/@me", headers={"Authorization": f"Bearer {token}"})
    new_data = new.json()
    if "id" in new_data:
        session['id'] = new_data['id']
        session['avatar'] = f"https://cdn.discordapp.com/avatars/{new_data['id']}/{new_data['avatar']}.png"
        session['username'] = new_data['username']
        return redirect(url_for('home_blueprint.index'))
    dashlog.error(f"Failed to obtain a user's profile.\n{new.json()}")
    return jsonify({"msg": "Failed to obtain user profile", "returned": new.json()})

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get("id"):
        return render_template( 'login/login.html')
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/logout')
def logout():
    del session['id']
    return redirect(url_for('base_blueprint.login'))

## Errors

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
