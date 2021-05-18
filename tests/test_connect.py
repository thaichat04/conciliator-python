from unittest import TestCase
import conciliator as cc
from tests.mocksession import ReplaySession
from requests import HTTPError

class TestConnect(TestCase):

    def test_badlogin(self):
        cc.session = ReplaySession()
        cc.session.storepath = 'data/auth_badlogin'
        with self.assertRaises(HTTPError):
            cc.connect("foo", "bar")


    def test_onetenant(self):
        cc.session = ReplaySession()
        cc.session.storepath = 'data/auth_onetenant'
        r = cc.connect("foo", "bar")
        self.assertTrue(r)

    def test_selectedtenant(self):
        cc.session = ReplaySession()
        cc.session.storepath = 'data/auth_selectedtenant'
        r = cc.connect("foo", "bar", "Dhatim SAS")
        self.assertTrue(r)

    def test_multipletenant(self):
        cc.session = ReplaySession()
        cc.session.storepath = 'data/auth_multipletenant'
        with self.assertRaises(ValueError):
            cc.connect("foo", "bar", "tenant")