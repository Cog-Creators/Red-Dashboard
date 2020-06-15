---
description: >-
  This guide is only for those who are running only one webserver.  If you are
  planning on running multiple, please follow the instructions on the other
  Launching page.
---

# Running the Webserver

{% hint style="warning" %}
**This tutorial requires you to have little amount of knowledge regarding hosting websites and servers if you want to use an URL, most especially if you want to use a subdomain!**
{% endhint %}

After you have installed the package and entered your environment, you can start the webserver with the command `reddash`. Once you type that command, it will launch the webserver, which should be viewable at the domain/IP specified in [Cog configuration with one bot](../cog-installation/cog-configuration-with-one-bot.md).

{% hint style="info" %}
Make sure to not go directly to the `/callback` endpoint.  It is not for going to directly, and instead only serves for when redirected by Discord during logon.
{% endhint %}

If you wish for the webserver to run with Automatic Startup, check out the [Automatic Startup \(systemctl\)](../webserver-installation/automatic-startup-systemctl.md) guide if you are on Linux.

## Interact with the bot

You may notice on the terminal that it says it is disconnected from RPC. If so, restart your bot adding the `--rpc` flag.  If you're using systemctl for starting Red, go to your configuration file, at the end of the line `ExecStart`, add the flag.  If this still does not work, refer to [Help & Support](../support/help-and-support.md) for a list of fixes.

In case you have not already, follow the instructions on [Installing the cog](../cog-installation/installing-cog.md) to install and configure the dashboard cog to work with the webserver.

