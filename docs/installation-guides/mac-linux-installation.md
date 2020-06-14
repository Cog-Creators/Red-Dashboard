---
description: >-
  This page is made for Mac/Linux users, do not follow this guide if you are on
  Windows or any other OS.
---

# Mac/Linux Installation

{% hint style="warning" %}
This webserver and it's accompanying cog is built for Red Discord Bot, and Red Discord Bot ONLY. It will not work with other bots. If you haven’t already, install Red [here](https://docs.discord.red/en/stable/).
{% endhint %}

Welcome to the Mac/Linux Installation Guide for the Red Discord Bot Dashboard Webserver. While running the below directions, the following is assumed:

* You are on a Mac or Linux distribution
* You have all pre-requisites of Red Discord Bot installed
* You have an instance of Red Discord Bot, set up and initialized

## Creating a virtual environment

{% hint style="info" %}
_Every time you start the webserver, you must enter your environment before starting it._
{% endhint %}

**A virtual environment is required for use/support. This helps prevent a multitude of issues, and this way you won't void support for your installation if you are not using a virtual environment.**

You have two options for creating the virtual environment, depending on how you installed Red/python:

1. Using [`pyenv virtualenv`](mac-linux-installation.md#using-pyenv-virtualenv) \(only available for those who installed `pyenv` when installing Red\)
2. Using [`venv`](mac-linux-installation.md#using-venv) \(available to anyone\)

### Using pyenv virtualenv

1. Open a terminal.
2. Type `pyenv virtualenv redashenv` to create a virtual environment.
3. Enter your environment with `pyenv shell redashenv`.
4. Type `python -m pip install Red-Dashboard`and let it install.

_You can continue to_ [_Launch Dashboard_](../launching-dashboard/running-the-webserver.md) _or_ [_Automatic Startup_](automatic-startup-systemctl.md)_._

### Using venv

1. Open a terminal.
2. Type `python3.8 -m venv ~/redashenv`to create a virtual environment.
3. Enter your environment with `source ~/redashenv/bin/activate`.
4. Type `python -m pip install Red-Dashboard` and let it install.

_You can continue to_ [_Launch Dashboard_](../launching-dashboard/running-the-webserver.md) _or_ [_Automatic Startup_](automatic-startup-systemctl.md)_._

