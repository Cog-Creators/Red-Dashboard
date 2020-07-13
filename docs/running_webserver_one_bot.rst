Running the Webserver
=====================

After you have installed the package and entered your environment, you
can start the webserver with the command ``reddash``. Once you type that
command, it will launch the webserver, which should be viewable at the
domain/IP specified in `Cog configuration with one bot <cog_config_one_bot>`.

If you wish for the webserver to run with Automatic Startup, check out
the `Automatic Startup (systemctl) <systemctl_startup>` guide if you
are on Linux.

Interact with the bot
---------------------

You may notice on the terminal that it says it is disconnected from RPC.
If so, restart your bot adding the ``--rpc`` flag. If you're using
systemctl for starting Red, go to your configuration file, at the end of
the line ``ExecStart``, add the flag. If this still does not work, refer
to `Help & Support <help_and_support>` for a list of fixes.

In case you have not already, follow the instructions on `Installing the cog <cog_installation>`
to install and configure the dashboard cog to work with the webserver.