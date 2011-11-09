Roan
====

Roan is a per-model url purging Django app. It connects to model signals and purge URLs wherever a model is saved, updated or deleted.

nginx proxy_cache support
=========================

Since Roan is based on a personal needing, it's based on nginx's `proxy_cache <http://wiki.nginx.org/HttpProxyModule#proxy_cache>`_.

Suppose you have the following purge mapping:

    location ~ /purge(/.*) {
        allow 127.0.0.1;
        allow 74.207.234.182;
        deny all;
        proxy_cache_purge fscom "$scheme://$host$1";
    }

Now suppose you have the following `Django <http://djangoproject.com>`_ model:

    class Post(models.Model):
        title = models.CharField(max_length=100)
        content = models.TextField()

And you have a URL ``/posts`` where users can see a list of posts. How can you set a forever cache and expect the cache to be refreshed
whenever a new post is saved? Or whenever a post gets updated or deleted?

Using Roan you'll be able to connect one or more models to one or more URL. So you can connect the ``Post`` model with the ``/posts`` URL,
and whenever a Post gets saved, updated or deleted, Roan makes an asynchronous request to the ``/purge/posts`` URL.
