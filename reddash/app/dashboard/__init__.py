# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

blueprint = Blueprint(
    "dashboard_blueprint", __name__, template_folder="templates", static_folder="static",
)
