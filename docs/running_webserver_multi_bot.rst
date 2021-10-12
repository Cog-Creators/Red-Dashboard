Running the Webserver with multiple bots
========================================

Take the list of ports you created in `Configuration Companion Cog - Multibot <configuration_guides/multibot>`.
It should look something like the below:

+-------------+------------+------------------+
| Bot         | RPC port   | Webserver port   |
+=============+============+==================+
| Redbot #1   | 6133       | 42356            |
+-------------+------------+------------------+
| Redbot #2   | 6134       | 42357            |
+-------------+------------+------------------+
| Redbot #3   | 6135       | 42358            |
+-------------+------------+------------------+

Now, for each bot follow these instructions:

1. Run ``reddash --port <webport> --rpc-port <rpcport>`` in your virtual
   environment, making sure to replace ``<webport>`` and ``<rpcport>``,
   respectively. For example, if I was running Redbot #3, I would start
   the webserver with ``reddash --port 42358 --rpc-port 6135``.
2. Start the respective bot with the following flags:
   ``--rpc --rpc-port <rpcport>``. For example, if I was starting Redbot
   #3, I would run ``redbot redbot3 --rpc --rpc-port 6135``.
3. After you do that, the webserver should be launched, and should be
   viewable at the domain/IP address specified in `Configuration Companion Cog - Multibot <configuration_guides/multibot>`.

.. tip::

   Make sure to not go directly to the ``/callback`` endpoint. It is not
   for going to directly, and instead only serves for when redirected by
   Discord during logon.

If you wish for the webserver to run with Automatic Startup, check out
the `Automatic Startup (systemctl) <systemctl_startup>` guide if you are on Linux.

.. warning::

   If you are running with systemctl, you must include the above flags on the ``ExecStart`` line.

If you notice in any terminals that it says it is disconnected from RPC,
make sure that you started the respective bot with the ``--rpc`` flag,
and passed the correct port to ``--rpc-port``. If this still does not,
refer to `Help & Support <help_and_support>` for a list of fixes.