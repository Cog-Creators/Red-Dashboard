Cog configuration with one bot
==============================

Welcome to the Dashboard Cog Configuration Guide. While running the
below directions, it is assumed that you have installed the dashboard
cog from the Toxic Cogs repository, and have loaded it, according to the
`Installing the cog <cog_installation>` guide.

Set the client secret
---------------------

The client secret is used so that the bot can obtain a user's profile
when logging in, and restricts what the user can do on the dashboard
according to their assigned permissions. The client secret is never used
maliciously, nor is user's data.

1. Login to the Discord Developer Console (found
   `here <https://discord.com/developers/applications>`__) and click on
   your bot's application.
2. Under your bot's name, on the right, there should be text that says
   "Client Secret" (NOT "Client ID"), and a "Copy" button underneath it.
3. Copy the secret to your clipboard by clicking the Copy button, then
   take the secret and paste it into the following command, replacing
   ``<secret>`` with it.

.. code-block:: none

    [p]dashboard settings oauth secret <secret>

.. tip:: 

   Keep the Discord Developer Console page open for later.

Set the redirect URL
--------------------

The redirect URL is where the user will be redirected after authorizing
the bot access to their profile. In order for the bot to process the
data correctly, the URL must be at the ``/callback`` endpoint of the
server.

Determine your redirect
~~~~~~~~~~~~~~~~~~~~~~~

There are two options for the redirect URL, however one of them is only
available under certain circumstances.

Option #1: Domain (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. attention:: 

   This option is only available of the following is true:

   1. You have a domain bought and set up, and are ready to connect it to
      the dashboard.
   2. You acknowledge that direct support will not be given for connecting
      the dashboard to the domain.

When running on a domain, the redirect should be something like
``https://domain.com/callback``. For example, if my domain was
``reddashboard.io``, my redirect would be
``https://reddashboard.io/callback``. Save this redirect to your
clipboard.

.. warning:: 

   **Warning! It is recommended to use a reverse proxy when setting up the dashboard. Check out** `Reverse proxying with Apache <reverse_proxy_apache>` **to get started, if you are on Linux.**

Option #2: Local/Private IP address
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. attention::

   This option is only available if the following is true:

   1. You only want the webserver accessible to you.
   2. You are running the webserver on a the same network as the computer
      you will access the dashboard from.

There are two options for the redirect URL in this situation, depending
on how you will be accessing the dashboard. Follow the step below
depending on which one you prefer:

-  Accessing the dashboard from the same device the bot is running on
   (Local):
-  Your redirect URL will be ``http://127.0.0.1:42356/callback``.
-  Accessing the dashboard from a different device the bot is running
   on, but on the same network (Private):
-  Your redirect URL will be ``http://ipaddress:42356/callback``.
   Replace ``ipaddress`` with your private IP address. For example, if
   my private IP address was ``192.168.1.2``, my redirect would be
   ``http://192.168.1.2:42356/callback``.

.. tip::

   You can find your private IP address by running ``ipconfig`` on Windows, or ``ifconfig`` on Mac/Linux.

Registering the redirect
~~~~~~~~~~~~~~~~~~~~~~~~

1. Copy the redirect URL as determined in the previous step to your
   clipboard, then paste into the command below, replacing
   ``<redirect>`` with the redirect:

.. code-block:: none

   [p]dashboard settings oauth redirect <redirect>

2. Switch back to the page for your application on the Discord Developer
   Console (the same page as earlier), click on the OAuth2 page on the
   left, then under the redirects, paste the redirect URL into one of
   the inputs.

.. important::

   The redirect set in the dashboard cog and the developer portal must be EXACTLY the same.

Register support server (Optional)
----------------------------------

You may want to have a link to your support server in case anybody needs
help with the dashboard. To do this, grab an invite link for your
server, and paste it into the command below, replacing ``<invite>`` with
the link to your server:

.. code-block:: none

    [p]dashboard settings support <invite>

*If you have not yet installed the webserver, head over to* `Mac/Linux Installation <mac_linux_installation>` *or* `*Windows Installation <windows_installation>` *, depending on your OS, to install it. If you already have, head over to* `Running the Webserver <running_webserver_one_bot>` *to finish up the process.*