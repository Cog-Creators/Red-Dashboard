# -*- encoding: utf-8 -*-
"""
License: Commercial
Copyright (c) 2019 - present AppSeed.us
"""

from reddash.app import create_app
import argparse

parser = argparse.ArgumentParser(description="Argument parser for Red Discord Bot Dashboard - Client")
parser.add_argument("--port", dest="port", type=int, default=42356)
parser.add_argument("--rpc-port", dest="rpcport", type=int, default=6133)
parser.add_argument("--interval", dest="interval", type=int, default=5, help=argparse.SUPPRESS)

args = vars(parser.parse_args())

if args['interval'] != 5:
    print("Detected interval argument.  Please note that this argument should only be used if you are explicitly told to use it.")

def main():
    args = vars(parser.parse_args())
    create_app("0.0.0.0", args['port'], args['rpcport'], args['interval'])

if __name__ == "__main__":
    main()