Help & Support
==============

.. danger::
    This project is **discontinued**, is no longer supported, and is known to
    be **completely non-functional**. If you are searching for a dashboard,
    please search the `Index <https://index.discord.red/>`_ for one in active
    development.

Common Questions
----------------

**Dashboard cog is loaded, and webserver is up, but it isn't showing my
bot's info**

-  Did you start the bot with the RPC flag?
-  If you started the bot with the ``--rpc-port`` flag, did you provide
   the same port to ``reddash``\ command when starting the webserver?  Vice versa?
-  Have you set the redirect and secret in the cog's settings?
-  Have you tried reloading the dashboard cog/restarting the webserver?
-  Have you tried updating the dashboard cog and dashboard itself?

**My browser said the website take too much time to answer or a similar
error**

Your firewall is maybe not configured to accept the port Dashboard is
listening for, if you are on Linux, run ``sudo ufw allow <webport>``
(Default is 42356). If you are on Windows, type ``Firewall`` in your
search bar and add a new rule.
