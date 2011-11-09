# -*- coding: utf-8 -*-

from django.db.models import signals


class purge(object):

    def __init__(self, url):
        self.url = url

    def on_save(self, model):
        def purger(sender, **kw):
            pass

        signals.post_save.connect(purger, sender=model, weak=False, dispatch_uid='purge_%s_for_%s' % (self.url, model._meta.verbose_name))
