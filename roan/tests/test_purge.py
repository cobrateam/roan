# -*- coding: utf-8 -*-
import unittest
import weakref

import requests
import roan

from django.conf import settings
from django.db.models import signals
from polls import models
from roan.tests import mocks


class PurgeTestCase(unittest.TestCase):

    def setUp(self):
        self.bkp_receivers_save = signals.post_save.receivers
        self.bkp_receivers_delete = signals.post_delete.receivers
        signals.post_save.receivers = []

        self.old_purge_url = getattr(settings, 'ROAN_PURGE_URL', None)
        if self.old_purge_url:
            del settings.ROAN_PURGE_URL

    def tearDown(self):
        signals.post_save.receivers = self.bkp_receivers_save
        signals.post_delete.receivers = self.bkp_receivers_delete

        if self.old_purge_url:
            settings.ROAN_PURGE_URL = self.old_purge_url
        elif hasattr(settings, 'ROAN_PURGE_URL'):
            del settings.ROAN_PURGE_URL

    def test_should_store_the_requests_module_in_the_local_object(self):
        p = roan.purge("/")
        self.assertEquals(requests, p.requests)

    def test_should_store_the_ROAN_PURGE_URL_setting_in_the_object(self):
        settings.ROAN_PURGE_URL = "http://google.com.br/purge"
        p = roan.purge("/")
        self.assertEquals("http://google.com.br/purge", p.purge_url)

    def test_should_remove_the_leading_slash_in_the_ROAN_PURGE_URL_if_its_present(self):
        settings.ROAN_PURGE_URL = "http://google.com.br/purge/"
        p = roan.purge("/")
        self.assertEquals("http://google.com.br/purge", p.purge_url)

    def test_should_use_default_purge_url_when_ROAN_PURGE_URL_is_not_present(self):
        p = roan.purge("/")
        self.assertEquals("http://localhost/purge", p.purge_url)

    def test_purge_should_receive_and_store_url(self):
        p = roan.purge("/")
        self.assertEquals("/", p.url)

    def test_purge_should_connect_to_save_signal_of_a_model_with_unique_dispatch_uid(self):
        roan.purge("/").on_save(models.Poll)
        expected_uid = "purge_/_post_save_%s" % models.Poll._meta.verbose_name
        uuids = [r[0][0] for r in signals.post_save.receivers]
        self.assertIn(expected_uid, uuids)

    def test_purge_should_connect_to_save_signal_without_a_weak_reference(self):
        uid = "purge_/_post_save_%s" % models.Poll._meta.verbose_name
        roan.purge("/").on_save(models.Poll)
        f = [r[1] for r in signals.post_save.receivers if r[0][0] == uid][0]
        self.assertNotIsInstance(f, weakref.ref)

    def test_when_the_model_is_saved_the_url_should_be_purged(self):
        purge_url = "http://localhost/purge/polls"
        p = roan.purge("/polls")
        p.requests = mocks.RequestsMock(200, purge_url)
        p.on_save(models.Poll)

        models.Poll.objects.create(title=u'Do you think Roan works well?')
        self.assertTrue(p.requests.done)

    def test_purge_should_connect_to_delete_signal_of_a_model_with_unique_dispatch_uid(self):
        roan.purge("/").on_delete(models.Poll)
        expected_uid = "purge_/_post_delete_%s" % models.Poll._meta.verbose_name
        uuids = [r[0][0] for r in signals.post_delete.receivers]
        self.assertIn(expected_uid, uuids)

    def test_purge_should_to_delete_sginal_without_a_weak_reference(self):
        uid = "purge_/_post_delete_%s" % models.Poll._meta.verbose_name
        roan.purge("/").on_delete(models.Poll)
        f = [r[1] for r in signals.post_delete.receivers if r[0][0] == uid][0]
        self.assertNotIsInstance(f, weakref.ref)

    def test_when_the_model_is_deleted_the_url_should_be_purged(self):
        purge_url = "http://localhost/purge/polls"
        p = roan.purge("/polls")
        p.requests = mocks.RequestsMock(200, purge_url)
        p.on_delete(models.Poll)

        poll = models.Poll.objects.create(title=u'Do you think Roan works well?')
        poll.delete()
        self.assertTrue(p.requests.done)

    def test_should_be_able_to_purge_an_url_on_save_a_model_instance(self):
        poll, created = models.Poll.objects.get_or_create(title=u'Do you think Roan should work?')

        purge_url = "http://localhost/purge/polls/%d" % poll.id
        p = roan.purge("/polls/%d" % poll.id)
        p.requests = mocks.RequestsMock(200, purge_url)
        p.on_save(poll)

        poll.title = u'Do you think Roan works?'
        poll.save()
        self.assertTrue(p.requests.done)

    def test_should_not_purge_on_saving_an_object_that_was_not_connected_to_the_url(self):
        poll, created = models.Poll.objects.get_or_create(title=u'Do you think Roan should work?')

        purge_url = "http://localhost/purge/polls/%d" % poll.id
        p = roan.purge("/polls/%d" % poll.id)
        p.requests = mocks.RequestsMock(200, purge_url)
        p.on_save(poll)

        models.Poll.objects.get_or_create(title=u'What is your favorite car?')
        self.assertFalse(p.requests.done)

    def test_should_be_able_to_purge_an_url_on_delete_a_model_instance(self):
        poll, created = models.Poll.objects.get_or_create(title=u'Do you think Roan should work?')

        purge_url = "http://localhost/purge/polls/%d" % poll.id
        p = roan.purge("/polls/%d" % poll.id)
        p.requests = mocks.RequestsMock(200, purge_url)
        p.on_delete(poll)

        poll.delete()
        self.assertTrue(p.requests.done)

    def test_should_not_purge_on_deleting_an_object_that_was_not_connected_to_the_url(self):
        poll, created = models.Poll.objects.get_or_create(title=u'Do you think Roan should work?')
        other, created = models.Poll.objects.get_or_create(title=u'What is your favorite car?')

        purge_url = "http://localhost/purge/polls/%d" % poll.id
        p = roan.purge("/polls/%d" % poll.id)
        p.requests = mocks.RequestsMock(200, purge_url)
        p.on_delete(poll)

        other.delete()
        self.assertFalse(p.requests.done)
