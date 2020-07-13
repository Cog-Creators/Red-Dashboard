Cog Installation
================

.. attention::

    This webserver and it's accompanying cog is built for Red Discord Bot, and Red Discord Bot ONLY. It will not work with other bots. If you haven’t already, install Red `here <https://docs.discord.red/en/stable/>`__.

Welcome to the Dashboard Cog Installation Guide. While running the below
directions, the following is assumed:

1. You have an active instance of Red Discord Bot, 3.3.9+ (you can check
   your version with ``[p]info``).
2. You have the ``downloader`` cog loaded.
3. ``[p]`` represents your prefix.

Installing the cog from the repository
--------------------------------------

1. First, if you have not already, add my repository to your bot:

.. code-block:: none

    [p]repo add toxic https://github.com/NeuroAssassin/Toxic-Cogs

2. Next, install the cog from the repo:

.. code-block:: none

    [p]cog install toxic dashboard

3. Finally, load the cog:

.. code-block:: none

    [p]load dashboard

*You can now proceed to the cog configuration pages. If you are running one webserver, please proceed to* `Cog configuration with one bot <cog_config_one_bot>` *. If you are running multiple, proceed to* `Cog configuration with multiple bots <cog_config_multi_bot>`.
