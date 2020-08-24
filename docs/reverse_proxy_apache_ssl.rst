Reverse Proxy with Apache (SSL) on Linux
========================================

This guide will show you how to setup the Apache webserver with SSL mod
and reverse proxy to the HTTPS protocol. Do note, that this guide is only
intended for users on the Linux Operating System and its distros. This
guide will use Debian 10 (Buster) as an example, please adapt according
to the distribution you are using.

Prerequisites
-------------

We're going to start off with making sure you have everything ready.

1. Logged in as a user with *sudo* privileges.
2. Access to your domain's DNS settings. In this case, we'll use *example.com*.
3. Apache and Certbot.

We'll go through in generating a self-signed SSL certificate from the
Let's Encrypt CA and apply it for the domain to encrypt traffic.

Apache and Certbot Installation
-------------------------------

If you do not have Apache and/or Certbot, run the following command.

.. code-block::

    sudo apt-get install apache2 certbot

Once it's finished, navigate to your server's IP address and you should
see the Apache default page. Let's go ahead and turn it off as we don't
need anyone coming in while we set things up.

.. code-block::

    sudo systemctl stop apache2

Generating SSL Certificate
--------------------------

