Automatic Startup (systemctl)
=============================

.. warning::

    This guide is for **Linux only.** There's is no auto-restart system for Windows or Mac at the moment.

.. warning::

    If you plan to run this with multiple bots, you will need to add the flags you normally add to the ExecStart line.  Additionally, if you have multiple systemctl files for the dashboard, you will need to rename them.


Creating the service file
-------------------------

In order to create the service file, you will first need to know two
things, your Linux ``username`` and your Python ``path``.

First, your Linux ``username`` can be fetched with the following
command:

.. code-block:: none

    whoami

Next, your python ``path`` can be fetched with the following commands:

.. code-block:: none

    # If reddash is installed in a venv
    source ~/redashenv/bin/activate
    which python

    # If reddash is installed in a pyenv virtualenv
    pyenv shell <virtualenv_name>
    pyenv which python

Then create the new service file:

``sudo -e /etc/systemd/system/redash.service``

Replace ``path`` with your python path and ``username`` with your Linux username.

.. code-block:: none

    [Unit]
    Description=Red Dashboard
    After=multi-user.target
    After=network-online.target
    Wants=network-online.target

    [Service]
    ExecStart=path -O -m reddash
    User=username
    Group=username
    Type=idle
    Restart=always
    RestartSec=15
    RestartPreventExitStatus=0
    TimeoutStopSec=10

    [Install]
    WantedBy=multi-user.target

Save your file and exit: ``ctrl + O; enter; ctrl + x``

Now you can start dashboard by using:

.. code-block:: none

    # Start Dashboard
    sudo systemctl start redash

    # Stop Dashboard
    sudo systemctl stop redash

Automatic startup on system bootup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To automatically start dashboard at system's bootup, use the following
command:

.. code-block:: none

    # Enable automatic startup
    sudo systemctl enable redash

    # Disable automatic startup
    sudo systemctl disable redash

Check logs
~~~~~~~~~~

To check Dashboard's logs, use:

.. code-block:: none

    sudo journalctl -eu redash

.. tip:: 

    You can use the ``--following`` flag to see live logs, to check if there's any trouble while using the dashboard.