Windows Installation
====================

.. attention::

   This webserver and it's accompanying cog is built for Red Discord Bot. It will not work with other bots. If you haven’t already, install Red `here <https://docs.discord.red/en/stable/>`__.

.. warning::

   For safety reasons, no commands in this guide should be run in a Command Prompt or Powershell session with Administrator privileges.  No installation commands require access to protected folders.

Welcome to the Windows Installation Guide for the Red Discord Bot
Dashboard Webserver. While running the below directions, the following
is assumed:

-  You are on a Windows distribution
-  You have all pre-requisites of Red Discord Bot installed
-  You have an instance of Red Discord Bot, set up and initialized

Installing the pre-requirements
-------------------------------

This guide recommends using the same requisites that Red - Discord Bot uses.  To ensure that you have the proper software already installed, consult the installation guide for your operating system `here <https://docs.discord.red/en/stable/install_guides/index.html>`__.

Creating a virtual environment
------------------------------

Just like for Red - Discord Bot, Red Dashboard requires it’s own, separate virtual environment to isolate dependencies.  Red Dashboard also requires a Python version minimum of 3.8.1, and it is recommended to use the same Python version as you use for Red - Discord Bot.

First, create a virtual environment using whatever Python version you use for red.  For example, if Python 3.8 was installed and being used for Red:

.. prompt:: batch

   py -3.8 -m venv "%userprofile%\reddashenv"

Next, enter your virtual environment with this command:

.. prompt:: batch

   "%userprofile%\reddashenv\Scripts\activate.bat"

.. important::

   You must activate the virtual environment with the above command every time you open a new shell to run, install or update Red Dashboard.

Installing Red Dashboard
------------------------

First, make sure you are in your virtual environment that you set up earlier by running the activation command mentioned above.

Once you are inside your virtual environment, update setup packages then install:

.. prompt:: batch
   :prompts: (reddashenv) C:\\>

   python -m pip install -U pip setuptools wheel
   python -m pip install -U Red-Dashboard

*You can continue to* `Installing Companion Cog <../configuration_guides/installing_companion_cog>`.