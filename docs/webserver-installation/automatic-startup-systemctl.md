---
description: To know how to start automatically Dashboard at every startup
---

# Automatic Startup \(systemctl\)

{% hint style="danger" %}
This guide is for **Linux only.** There's actually no auto-restart system for Windows or Mac at the moment.
{% endhint %}

{% hint style="warning" %}
This tutorial does not support multiples bots running.
{% endhint %}

If you wonder what is systemctl, systemctl is a controlling interface and inspection tool for the widely-adopted init system and service manager systemd.

## Creating the service file

In order to create the service file, you will first need to know two things, your Linux `username` and your Python `path`

First, your Linux `username` can be fetched with the following command:

```text
whoami
```

Next, your python `path` can be fetched with the following commands:

```text
# If reddash is installed in a venv
source ~/redashenv/bin/activate
which python

# If reddash is installed in a pyenv virtualenv
pyenv shell <virtualenv_name>
pyenv which python
```

Then create the new service file:

`sudo -e /etc/systemd/system/redash.service`

Replace `path` by what your python path and `username` by your Linux username

```text
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
```

Save your file and exit: `ctrl + O; enter; ctrl + x`

Now you can start dashboard by using:

```text
# Start Dashboard
sudo systemctl start redash

# Stop Dashboard
sudo systemctl stop redash
```

### Automatic startup on system bootup

To automatically start dashboard at system's bootup, use the following command:

```text
# Enable automatic startup
sudo systemctl enable redash

# Disable automatic startup
sudo systemctl disable redash
```

### Check logs

To check Dashboard's logs, use:

```text
sudo journalctl -eu redash
```

{% hint style="success" %}
You can use the `--following` flag to check if there's any trouble while using the dashboard.
{% endhint %}

