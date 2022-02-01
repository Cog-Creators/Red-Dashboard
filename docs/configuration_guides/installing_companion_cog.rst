Installing Companion Cog
========================

.. attention::

   This webserver and it's accompanying cog is built for Red Discord Bot. It will not work with other bots. If you haven’t already, install Red `here <https://docs.discord.red/en/stable/>`__.

Welcome to the Dashboard Cog Installation Guide. While running the below directions, the following is assumed:

1. You have an active instance of Red Discord Bot, 3.3.9+ (you can check your version with ``[p]info``).
2. You are considered a "bot owner" on your Red instance, meaning you can run owner-only commands.

Installing the cog from the repository
--------------------------------------

Installing the cog is extremely easy, and can be accomplished through Red's plugin, or cog system.

1. First, if you have not already, load the ``downloader`` cog on your bot:

.. tip::

    ``[p]`` represents your bot's prefix.  Make sure to replace it when pasting these commands inside of Discord.

.. code-block:: none

    [p]load downloader

2. Next, add Neuro Assassin's cog repository to your bot:

.. code-block:: none

    [p]repo add NeuroAssassin https://github.com/NeuroAssassin/Toxic-Cogs

.. danger::

    The ``dashboard`` cog located `here <https://github.com/NeuroAssassin/Toxic-Cogs>`__ is the only official companion cog to the Red Dashboard software.  Take precaution before installing cogs that you may not trust.

3. Next, install the ``dashboard`` cog from the repository:

.. code-block:: none

    [p]cog install NeuroAssassin dashboard

4. Finally, load the ``dashboard`` cog:

.. code-block:: none

    [p]load dashboard

*You can now proceed to configuration the companion dashboard cog.  Start* `here <index>` *to decide which guide to follow.*