---
description: You can receive support here if you got any troubles while using dashboard.
---

# Help & Support

## Support Server

{% hint style="danger" %}
As said before, this cog is in very early stage development, and is not intended for public use, and I am looking for **bugs**, **issues** and **feedback**. If you cannot understand the \(relatively simple\) instructions, then now is not a good time to install, and its better to wait until it is officially released. I would recommend searching google for the answers to your questions. If for some reason, you cannot understand how to install it at all, and I warn, ONLY if it is that, then you can DM Draper from the Red server.
{% endhint %}

> [Link to the support server](https://discord.gg/vQZTdB9)

## Common Questions

**Dashboard cog is loaded, and webserver is up, but it isn't showing my bot's info**

* Did you start the bot with the RPC flag?
* If you started the bot with the `--rpc-port` flag, did you provide the same port to `reddash`command when starting the webserver?
* Have you set the redirect and secret in the cog's settings?
* Have you tried reloading the dashboard cog/restarting the webserver?
* Have you tried updating the dashboard cog and dashboard itself?

**My browser said the website take too much time to answer or a similar error**

Your firewall is maybe not configured to accept the port Dashboard is listening for, if you are on Linux, run `sudo ufw allow <Port>` \(Default is 42356\). If you are on Windows, type `Firewall` in your search bar and add a new rule.

