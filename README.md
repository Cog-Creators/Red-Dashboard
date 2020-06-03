# Red-Dashboard
*An easy-to-use interactive web dashboard to control your Redbot.*

## Installation
A virtual environment is required for use/support.  Follow the documentation below (based upon Red Discord Bot documentation) according to your OS.

> :warning: Every time you start the webserver, you must enter your environment before starting it.

### Windows
1. Start by opening up a Command Prompt (click on Search and type `cmd`).
2. Type `py -3.8 -m venv "%userprofile%\redashenv"` to create the environment.
3. Enter your environment by typing `"%userprofile%\redashenv\Scripts\activate.bat"`.
4. Type `python -m pip install Red-Dashboard` and let it install.

### Mac / Linux
1. Open a terminal.
2. Type `python3.8 -m venv ~/redashenv`.
3. Enter your environment with `source ~/redashenv/bin/activate`.
4. Type `python -m pip install Red-Dashboard` and let it install.

## Running the webserver

### Running the webserver with one bot
After you have installed the package, you can start the webserver with the command `reddash`.  Once you type that command, it will launch the webserver and be open on your device's IP address.  If you are on the same device, you can view it at http://127.0.0.1:42356 or at your computer's local or public IP address at http://ip.add.re.ss:42356.  If you are on a different device, you must use the device's public IP address and set up a port forwarding rule (unless your VPS does it for you).

> To find your public IP address, google "what is my ip".

### Running the webserver with multiple bots
If you are running multiple webservers for multiple bots, it will be a little bit more tricky.  First off, create two port numbers between 1 and 65,535 for each bot, and choose one for RPC (from now on referred to as `<rpcport>`) and one for webserver port (from now on referred to as `<webport>`).

> :warning: It is recommended to choose ports with higher numbers, as lower numbered ports are frequently used by other processes.

> If you have already made a list of ports when following the instructions for the dashboard cog on the Toxic Cogs repository, USE THOSE INSTEAD.

Now, for each bot that you want to have a webserver for, run this command: `reddash --port <webport> --rpc-port <rpcport>`, making sure to replace `<webport>` and `<rpcport>`, respectively.

Now, to view the dashboard, go to `http://127.0.0.1:<webport>` if on the same device, or to `http://ip.add.re.ss:<webport>` (replacing `ip.add.re.ss` with your public IP address).

> To find your public IP address, google "what is my ip".

## Connecting the webserver to the bot
In case you have not already, install the Dashboard cog on the Toxic-Cogs repository, and configure it by following the instructions on the README there.

## Issues
If you have any issues installing or running, feel free to stop by my support server.

[![Discord server](https://discordapp.com/api/guilds/540613833237069836/embed.png?style=banner3)](https://discord.gg/vQZTdB9)

## Credits
I would like to thank the following, for all the contributions they have made that helped this become what it is today.
* Cog Creators, for making such an amazing bot.
* All the people who tested the dashboard, and gave feedback.
* AppSeed, for creating a template that I use as the base for the Dashboard.
