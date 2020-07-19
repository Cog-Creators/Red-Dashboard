# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint, abort, request, redirect, url_for, session
from reddash.app import app
import locale

blueprint = Blueprint(
    "home_blueprint",
    __name__,
    url_prefix="/<lang_code>",
    template_folder="templates",
    static_folder="static",
)


@blueprint.url_defaults
def add_language_code(endpoint, values):
    values.setdefault("lang_code", session.get("lang_code"))


@blueprint.url_value_preprocessor
def pull_lang_code(endpoint, values):
    lang = values.pop("lang_code")
    if lang in locale.locale_alias:
        session["lang_code"] = lang


@blueprint.before_request
def before_request():
    if session.get("lang_code") not in app.config["LANGUAGES"]:
        adapter = app.url_map.bind("")
        try:
            endpoint, args = adapter.match("/en" + request.full_path.rstrip("/ ?"))
            return redirect(url_for(endpoint, **args), 301)
        except:
            abort(404)

    dfl = request.url_rule.defaults
    if "lang_code" in dfl:
        if dfl["lang_code"] != request.full_path.split("/")[1]:
            abort(404)
