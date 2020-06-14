# Running the Webserver

{% hint style="warning" %}
**This tutorial requires you to have little amount of knowledge regarding hosting websites and servers if you want to use an URL, most especially if you want to use a subdomain!**
{% endhint %}

## Start Red the good way

In order to use Dashboard, your Red instance MUST start with the included RPC server. To start Red with the RPC server, you have to parse the `--rpc` flag.  
If you're using systemctl for starting Red, go to your configuration file, at the end of the line `ExecStart`, add the flag.

## Run Dashboard

After you have installed the package and entered your environment, you can start the webserver with the command `reddash`. Once you type that command, it will launch the webserver and be open on your device's IP address. If you are on the same device, you can view it at [http://127.0.0.1:42356](http://127.0.0.1:42356/) or at your computer's local or public IP address at http://ipaddress:42356.

If you are on a different device, you must use the device's public IP address and set up a port forwarding rule \(unless your VPS does it for you\).

> To find your public IP address, google "what is my ip".

## Interact with the bot

In case you have not already, install the Dashboard cog on the [Toxic-Cogs repository](https://github.com/NeuroAssassin/Toxic-Cogs), and configure it by following the instructions on the [README](https://github.com/NeuroAssassin/Toxic-Cogs/blob/master/dashboard/README.md) there.

