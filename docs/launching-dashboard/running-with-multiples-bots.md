---
description: This tutorials is made for peoples who use more than one Red's instances.
---

# Running the Webserver with multiple bots

{% hint style="warning" %}
**This tutorial requires you to have little amount of knowledge regarding hosting websites and servers if you want to use an URL, most especially if you want to use a subdomain!**
{% endhint %}

Take the list of ports you created in [Cog configuration with multiple bots](../cog-installation/cog-configuration-with-multiple-bots.md).  It should look something like the below:

| Bot | RPC port | Webserver port |
| :--- | :--- | :--- |
| Redbot \#1 | 6133 | 42356 |
| Redbot \#2 | 6134 | 42357 |
| Redbot \#3 | 6135 | 42358 |

Now, for each bot follow these instructions:

1. Run `reddash --port <webport> --rpc-port <rpcport>` in your virtual environment, making sure to replace `<webport>` and `<rpcport>`, respectively.  For example, if I was running Redbot \#3, I would start the webserver with `reddash --port 42358 --rpc-port 6135`.
2. Start the respective bot with the following flags: `--rpc --rpc-port <rpcport>`.  For example, if I was starting Redbot \#3, I would run `redbot redbot3 --rpc --rpc-port 6135`.
3. After you do that, the webserver should be launched, and should be viewable at the domain/IP address specified in [Cog configuration with multiple bots](../cog-installation/cog-configuration-with-multiple-bots.md).

{% hint style="info" %}
Make sure to not go directly to the `/callback` endpoint.  It is not for going to directly, and instead only servers for when redirecting by Discord.
{% endhint %}

If you wish for the webserver to run with Automatic Startup, check out the [Automatic Startup \(systemctl\)](../webserver-installation/automatic-startup-systemctl.md) guide if you are on Linux.

{% hint style="danger" %}
If you are running with systemctl, you must include the above flags on the `ExecStart` line.
{% endhint %}

If you notice in any terminals that it says it is disconnected from RPC, make sure that you started the respective bot with the `--rpc` flag, and passed the correct port to `--rpc-port`.  If this still does not, refer to [Help & Support](../support/help-and-support.md) for a list of fixes.

