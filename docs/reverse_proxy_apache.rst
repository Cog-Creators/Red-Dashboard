Reverse proxying with Apache on Linux
=====================================

Welcome to the Apache reverse proxy guide.  Note that this guide is meant
only for Linux users, and that currently there are no options for Windows
or Mac.  These commands will not work on those OSs, so do not follow this
if you are not on a Linux distribution.

Installing Apache
-----------------

1. Start off by updating your package index

.. code-block:: none

    sudo apt update

2. Next, install the apache2 package

.. code-block:: none

    sudo apt install apache2

At this point, if you navigate to your device's IP address, you should see an Apache welcome page.

Set up reverse proxy
--------------------

You probably don't want people visiting your domain to see that static Apache welcome page.
Now we need to configure apache to reverse proxy port 42356, or whichever port
your webserver is running on.

1. Create a host configuration file for your domain:

.. code-block:: none

    sudo nano /etc/apache2/sites-available/redash.conf

2. Paste the following into the file, replacing ``your.domain.com`` with the domain you will
be running the dashboard on.  Note that if you are running the webserver on a port other than
port 42356, you will need to replace ``42356`` below with the the specified port.

.. code-block:: none

    <VirtualHost *:80>
        ServerName your.domain.com
        ProxyPreserveHost On
        ProxyPass / http://0.0.0.0:42356/
        ProxyPassReverse / http://0.0.0.0:42356/
    </VirtualHost>

3. Enable the Apache modifications needed to reverse proxy

.. code-block:: none

    sudo a2enmod proxy
    sudo a2enmod proxy_http

4. Enable the new host configuration file and disable the default

.. code-block:: none

    sudo a2ensite redash.conf
    sudo a2dissite 000-default.conf

5. Finally, restart apache for the changes to take effect

.. code-block:: none

    sudo systemctl restart apache2

Now, if you navigate to your device's IP, you should be able to see the dashboard (if the
webserver is running).