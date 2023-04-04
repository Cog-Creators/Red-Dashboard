# -*- encoding: utf-8 -*-
"""
License: Commercial
Copyright (c) 2019 - present AppSeed.us
"""

from reddash.app import create_app
import argparse
import logging
from rich.console import Console
from rich.logging import RichHandler
import os
import sys

if sys.stdin.isatty():
    os.system("cls" if os.name == "nt" else "clear")

os.environ["WERKZEUG_RUN_MAIN"] = "true"

console = Console()

logging.basicConfig(format="%(message)s", handlers=[RichHandler()])

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

dashlog = logging.getLogger("reddash")
dashlog.setLevel(logging.WARNING)

parser = argparse.ArgumentParser(
    description="Argument parser for Red Discord Bot Dashboard - Client"
)
parser.add_argument("--host", dest="host", type=str, default="0.0.0.0")
parser.add_argument("--port", dest="port", type=int, default=42356)
parser.add_argument("--rpc-port", dest="rpcport", type=int, default=6133)
parser.add_argument("--interval", dest="interval", type=int, default=10, help=argparse.SUPPRESS)
parser.add_argument("--debug", dest="debug", action="store_true")
parser.add_argument("--development", dest="dev", action="store_true", help=argparse.SUPPRESS)

parser.add_argument("--instance", dest="instance", type=str, default=None)


def main():
    args = vars(parser.parse_args())

    if args["interval"] != 10:
        console.print(
            (
                "Detected interval argument.  Please note that this argument should "
                "only be used if you are explicitly told to use it."
            ),
            style="bold red",
        )

    if args["dev"]:
        console.print(
            (
                "Detected development status.  Please note that this argument is only for testing."
                " Do not use if you are opening this up to other people, as it can cause security "
                "issues. Confirm that you wish to run the webserver in developmental status by "
                "typing 'I agree', case sensitive, below:\n",
            ),
            style="bold red",
        )
        confirm = input("> ")
        print("")
        if confirm == "I agree":
            console.print(
                "User has read the warnings and has agreed. Launching developmental server.",
                style="bold red",
            )
        else:
            console.print(
                'User did not type "I agree".  Launching production server.',
                style="bold red",
            )
            args["dev"] = False

    create_app(
        args["host"],
        args["port"],
        args["rpcport"],
        args["interval"],
        args["debug"],
        args["dev"],
        args["instance"],
    )


if __name__ == "__main__":
    main()
