# -*- coding: utf-8 -*-
import unittest
import weakref

import roan

from django.db.models import signals
from polls import models


class PurgeTestCase(unittest.TestCase):

    def setUp(self):
        self.bkp_receivers = signals.post_save.receivers
        signals.post_save.receivers = []

    def tearDown(self):
        signals.post_save.receivers = self.bkp_receivers

    def test_purge_should_receive_and_store_url(self):
        p = roan.purge("/")
        self.assertEquals("/", p.url)

    def test_purge_should_connect_to_save_signal_of_a_model_with_unique_dispatch_uid(self):
        roan.purge("/").on_save(models.Poll)
        expected_uid = "purge_/_for_%s" % models.Poll._meta.verbose_name
        uuids = [r[0][0] for r in signals.post_save.receivers]
        self.assertIn(expected_uid, uuids)

    def test_purge_should_connect_to_save_signal_withou_a_weak_reference(self):
        uid = "purge_/_for_%s" % models.Poll._meta.verbose_name
        roan.purge("/").on_save(models.Poll)
        f = [r[1] for r in signals.post_save.receivers if r[0][0] == uid][0]
        self.assertNotIsInstance(f, weakref.ref)
