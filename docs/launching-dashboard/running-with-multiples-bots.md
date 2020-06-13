# Running with multiples bots

{% hint style="warning" %}
**This tutorial requires you to have little amount of knowledge regarding hosting websites and servers if you want to use an URL, most especially if you want to use a subdomain!**
{% endhint %}

If you are running multiple webservers for multiple bots, it will be a little bit more tricky. First off, create two different RPC port numbers between 1 and 65,535 for each bot using `--rpcport`flag, and choose one for RPC \(from now on referred to as `<rpcport>`\) and one for webserver port \(from now on referred to as `<webport>`\).

{% hint style="danger" %}
It is recommended to choose ports with higher numbers, as lower numbered ports are frequently used by other processes.
{% endhint %}

> If you have already made a list of ports when following the instructions for the dashboard cog on the Toxic Cogs repository, USE THOSE INSTEAD.

Now, for each bot that you want to have a webserver for, run this command: `reddash --port <webport> --rpc-port <rpcport>`, making sure to replace `<webport>` and `<rpcport>`, respectively.

Now, to view the dashboard, go to `http://127.0.0.1:<webport>` if on the same device, or to `http://ip.add.re.ss:<webport>` \(replacing `ip.add.re.ss` with your public IP address\).

> To find your public IP address, google "what is my ip".

