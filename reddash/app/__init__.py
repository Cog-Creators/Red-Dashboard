# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
Copyright (c) 2020 - NeuroAssassin
"""
# Flask related libraries
from flask import Flask
from flask_babel import Babel
from waitress import serve

# Terminal related libraries
from rich import console, traceback as rtb, logging as richlogging
import logging

# Secret key libraries
import base64

# Base libraries
from datetime import datetime
from babel import Locale
import threading

# Relative imports
from reddash.app.data_manager import LoadManager
from reddash.app.tasks import TaskManager
from reddash.app.utils import (
    register_blueprints,
    apply_themes,
    add_constants,
    initialize_babel,
    startup_message,
)


# Logging and terminal set up

log = logging.getLogger("werkzeug")
dashlog = logging.getLogger("reddash")
queuelog = logging.getLogger("waitress.queue")

console = console.Console()
oldexcepthook = rtb.install()

logging.basicConfig(
    format="%(message)s", handlers=[richlogging.RichHandler(console=console, rich_tracebacks=True)]
)
queuelog.setLevel(logging.ERROR)

# Base variable setup
app = Flask("reddash", static_folder="app/base/static")
lock = threading.Lock()
babel = Babel()


def create_app(host, port, rpcport, interval, debug, dev, instance):
    if debug:
        log.setLevel(logging.DEBUG)
        dashlog.setLevel(logging.DEBUG)

    # Initialize websocket variables
    app.ws = None
    app.lock = lock

    # Initialize core variables
    app.console = console
    app.task_manager = TaskManager(app, console)
    app.running = True
    app.cooldowns = {
        "serverprefix": {},
        "adminroles": {},
        "modroles": {},
        "fetchrules": {},
        "fetchtargets": {},
        "fetchcogcommands": {},
        "addrule": {},
        "adddefaultrule": {},
        "removerule": {},
        "removedefaultrule": {},
        "fetchaliases": {},
    }

    # Initialize config
    app.data = LoadManager(instance=instance)
    app.data.initialize()

    app.config.from_object(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "app/translations"
    app.config["WEBSOCKET_HOST"] = "localhost"
    app.config["WEBSOCKET_PORT"] = rpcport
    app.config["WEBSOCKET_INTERVAL"] = interval
    app.config["RPC_CONNECTED"] = False
    app.config["LAST_RPC_EVENT"] = datetime.utcnow()
    app.config["LAUNCH"] = datetime.utcnow()

    app.config["LANGUAGES"] = [
        "en",
        "af_ZA",
        "ar_SA",
        "bg_BG",
        "ca_ES",
        "cs_CZ",
        "da_DK",
        "de_DE",
        "el_GR",
        "es_ES",
        "fi_FI",
        "fr_FR",
        "he_IL",
        "hu_HU",
        "id_ID",
        "it_IT",
        "ja_JP",
        "ko_KR",
        "nl_NL",
        "nb_NO",
        "pl_PL",
        "pt_BR",
        "pt_PT",
        "ro_RO",
        "ru_RU",
        "sk_SK",
        "sv_SE",
        "tr_TR",
        "uk_UA",
        "vi_VN",
        "zh_CN",
        "zh_HK",
        "zh_TW",
    ]
    locale_dict = {}

    for locale in app.config["LANGUAGES"]:
        loc = Locale.parse(locale)
        lang = loc.get_language_name(locale)
        if territory := loc.get_territory_name(locale):
            lang = f"{lang} - {territory}"
        locale_dict[locale] = lang
    app.config["LOCALE_DICT"] = locale_dict

    babel = Babel(app)

    # Initialize core app functions
    register_blueprints(app)
    apply_themes(app)
    add_constants(app)
    initialize_babel(app, babel)

    # Initialize security
    # Session encoding
    fernet_key = app.data.core["secret_key"]
    secret_key = base64.urlsafe_b64decode(fernet_key)

    # JWT encoding
    jwt_fernet_key = app.data.core["jwt_secret_key"]
    jwt_secret_key = base64.urlsafe_b64decode(jwt_fernet_key)

    app.secret_key = secret_key
    app.jwt_secret_key = jwt_secret_key

    kwargs = {"host": host, "port": port, "dev": dev, "debug": debug}
    startup_message(app, kwargs)

    app.task_manager.start_tasks()

    if dev:
        app.run(host=host, port=port, debug=debug)
    else:
        serve(app, host=host, port=port, _quiet=True)

    dashlog.fatal("Shutting down...")
    app.running = False
    app.task_manager.stop_tasks()

    dashlog.fatal("Webserver terminated")
    # For some reason, this exits on the same line sometimes.  Let's print an extra line
    print("")
