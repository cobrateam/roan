# -*- coding: utf-8 -*-
import requests

from django.conf import settings
from django.db.models import signals


class purge(object):

    def __init__(self, url):
        self.url = url
        self.purge_url = getattr(settings, "ROAN_PURGE_URL", "http://localhost/purge").rstrip("/")
        self.requests = requests

    def on_save(self, model):
        def purger(sender, **kw):
            purge_url = self.purge_url + self.url
            self.requests.get(purge_url)

        signals.post_save.connect(purger, sender=model, weak=False, dispatch_uid='purge_%s_for_%s' % (self.url, model._meta.verbose_name))
