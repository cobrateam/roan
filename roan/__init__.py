# -*- coding: utf-8 -*-
import requests

from django.conf import settings
from django.db import models as django_models
from django.db.models import signals


class purge(object):

    def __init__(self, url):
        self.url = url
        self.purge_url = getattr(settings, "ROAN_PURGE_URL", "http://localhost/purge").rstrip("/")
        self.requests = requests

    def _purge_instance(self, obj, signal):
        def purger(sender, instance, **kw):
            if instance == obj:
                purge_url = self.purge_url + self.url
                self.requests.get(purge_url)

        model = type(obj)
        signal.connect(purger, sender=model, weak=False, dispatch_uid='purge_%s_on_save_%s' % (self.url, model._meta.verbose_name))

    def _purge_class(self, model, signal):
        def purger(sender, **kw):
            purge_url = self.purge_url + self.url
            self.requests.get(purge_url)

        signal.connect(purger, sender=model, weak=False, dispatch_uid='purge_%s_on_save_%s' % (self.url, model._meta.verbose_name))

    def on_save(self, obj):
        if isinstance(obj, django_models.Model):
            self._purge_instance(obj, signals.post_save)
        else:
            self._purge_class(obj, signals.post_save)

    def on_delete(self, model):
        def purger(sender, **kw):
            purge_url = self.purge_url + self.url
            self.requests.get(purge_url)

        signals.post_delete.connect(purger, sender=model, weak=False, dispatch_uid='purge_%s_on_delete_%s' % (self.url, model._meta.verbose_name))
