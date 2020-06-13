---
description: >-
  This page is made for Windows user, do not follow this guide if you are on
  Linux or any other OS.
---

# Windows Installation

{% hint style="warning" %}
This webserver and it's accompanying cog is built for Red Discord Bot, and Red Discord Bot ONLY. It will not work with other bots. If you haven’t already, install Red [here](https://docs.discord.red/en/stable/).
{% endhint %}

Welcome to the Windows Installation Guide for the Red Discord Bot Dashboard Webserver. While running the below directions, the following is assumed:

* You are on a Windows distribution
* You have all pre-requisites of Red Discord Bot installed
* You have an instance of Red Discord Bot, set up and initialized

## Creating a virtual environment

{% hint style="info" %}
_Every time you start the webserver, you must enter your environment before starting it._
{% endhint %}

**A virtual environment is required for use/support. This helps prevent a multitude of issues, and thus you void support for your installation if you are not using a virtual environment.**

1. Start by opening up a Command Prompt \(click on Search and type `cmd`\).
2. Type `py -3.8 -m venv "%userprofile%\redashenv"` to create the environment.
3. Enter your environment by typing `"%userprofile%\redashenv\Scripts\activate.bat"`.
4. Type `python -m pip install Red-Dashboard` and let it install.

_You can continue to_ [_Launch Dashboard_](../launching-dashboard/untitled.md)_._

