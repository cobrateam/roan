Roan
====

Roan is a per-model url purging Django app. It connects to model signals and purge URLs wherever a model is saved, updated or deleted.

Getting started
---------------

Installation
++++++++++++

You can install ``Roan`` using pip:

::

    $ [sudo] pip install roan

The only dependency is `requests <http://python-requests.org>`_, that will be installed automatically by ``pip`` (if you don't use the ``--no-deps`` argument).

Configuration
+++++++++++++

``Roan`` uses only an optional setting: ``ROAN_PURGE_URL``. If you don't specify it, it'll be ``http://localhost/purge``.

Example of configuration:

::

    ROAN_PURGE_URL = 'http://nginx.souza.cc/clean'

nginx proxy_cache support
-------------------------

Since Roan is based on a personal need, it's based on nginx's `proxy_cache <http://wiki.nginx.org/HttpProxyModule#proxy_cache>`_.

Suppose you have the following purge mapping:

::

    location ~ /purge(/.*) {
        allow 127.0.0.1;
        deny all;
        proxy_cache_purge roan "$scheme://$host$1";
    }

Now suppose you have the following `Django <http://djangoproject.com>`_ model:

::

    class Post(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()

And you have a URL ``/posts`` where users can see a list of posts. How can you set a forever cache and expect the cache to be refreshed
whenever a new post is saved? Or whenever a post gets updated or deleted?

Using Roan you'll be able to connect one or more models to one or more URL. So you can connect the ``Post`` model with the ``/posts`` URL,
and whenever a Post gets saved, updated or deleted, Roan makes a request to the ``/purge/posts`` URL.

Usage
-----

Once you have Roan installed and configured, you just need to call it in a file that Django executes (e.g.: the ``models.py`` of your app).
Here is the code for the example above, of purging the ``/posts`` URL whenever a post gets saved or deleted:

::

    from roan import purge
    from models import Post

    purge("/posts").on_save(Post)
    purge("/posts").on_delete(Post)
