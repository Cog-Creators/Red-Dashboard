Mac/Linux Installation
======================

.. attention::

   This webserver and it's accompanying cog is built for Red Discord Bot, and Red Discord Bot ONLY. It will not work with other bots. If you haven’t already, install Red `here <https://docs.discord.red/en/stable/>`__.

Welcome to the Mac/Linux Installation Guide for the Red Discord Bot
Dashboard Webserver. While running the below directions, the following
is assumed:

-  You are on a Mac or Linux distribution
-  You have all pre-requisites of Red Discord Bot installed
-  You have an instance of Red Discord Bot, set up and initialized

Creating a virtual environment
------------------------------

.. tip::

   Every time you start the webserver, you must enter your environment before starting it.

**A virtual environment is required for use/support. This helps prevent
a multitude of issues, and this way you won't void support for your
installation if you are not using a virtual environment.**

You have two options for creating the virtual environment, depending on
how you installed Red/Python:

1. :ref:`using-pyenv-virtualenv` (only available for those who installed ``pyenv`` when installing Red)
2. :ref:`using-venv` (available to anyone)

.. _using-pyenv-virtualenv:

Using pyenv virtualenv
~~~~~~~~~~~~~~~~~~~~~~

1. Open a terminal.
2. Type ``pyenv virtualenv redashenv`` to create a virtual environment.
3. Enter your environment with ``pyenv shell redashenv``.
4. Type ``python -m pip install -U setuptools wheel``.
5. Type ``python -m pip install Red-Dashboard`` and let it install.

*You can continue to* `Installing the cog <cog_installation>` *or* `Automatic Startup <systemctl_startup>`.

.. _using-venv:

Using venv
~~~~~~~~~~

1. Open a terminal.
2. Type ``python3.8 -m venv ~/redashenv``\ to create a virtual
   environment.
3. Enter your environment with ``source ~/redashenv/bin/activate``.
4. Type ``python -m pip install -U setuptools wheel``.
5. Type ``python -m pip install Red-Dashboard`` and let it install.

*You can continue to* `Installing the cog <cog_installation>` *or* `Automatic Startup <systemctl_startup>`.
