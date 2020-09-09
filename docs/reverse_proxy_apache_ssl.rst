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

If you do not have Apache installed already, use the following commands in your
linux terminal:

.. code-block::

    sudo apt-get update
    sudo apt-get install apache2

The EFF has a great resource for installing *certbot* on your specific OS.

To begin, go to `EFF Certbot Website <https://certbot.eff.org/instructions>`__,
select your webserver software and what OS you are running. Afterwards, follow 
the instructions given to get certbot installed.

The SSL certificates generated are self-signed, and for our purposes, will
be just fine. If you want to use a certificate from a Certificate Authority,
the process will be slightly different.

Setting Up Apache For SSL
-------------------------


Apache Reverse Proxy
--------------------