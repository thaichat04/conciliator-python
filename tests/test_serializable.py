from unittest import TestCase
from conciliator.conciliatorobj import ConciliatorObj
import datetime


class TestSerializable(TestCase):

    class TestClass(ConciliatorObj):
        id: str
        nb: int
        isBool: bool
        created: datetime.date
        ts_tz: datetime.datetime
        ts_iso: datetime.datetime
        ts_notrailingzeros: datetime.datetime
        ts_badformat: datetime.datetime

    data = {'id': 'abc', 'nb': 1,'isBool': 'True', 'created': '2020-11-12',
            'ts_tz': '2020-10-20T16:40:40.036783Z',
            'ts_iso': '2020-10-20T16:40:40.036783',
            'ts_notrailingzeros': '2020-10-20T16:40:40.036',
            'ts_badformat': 'notatimestamp',
            'garbage': 'undeclared',
            'subclassprop': 'subvalue'}

    def test_deserialize(self):
        o = self.TestClass(self.data.copy())

        self.assertTrue((isinstance(o.id, str)))
        self.assertEqual(o.id, 'abc')
        self.assertTrue(isinstance(o.nb, int))
        self.assertEqual(o.nb, 1)
        self.assertEqual(o.created.isoformat(), '2020-11-12')
        self.assertEqual(o.ts_tz.isoformat(), '2020-10-20T16:40:40.036783+00:00')
        self.assertEqual(o.ts_iso.isoformat(), '2020-10-20T16:40:40.036783')
        self.assertEqual(o.ts_notrailingzeros.isoformat(), '2020-10-20T16:40:40.036000')
        with self.assertRaises(AttributeError):
            o.ts_badformat
        with self.assertRaises(AttributeError):
            o.garbage
        with self.assertRaises(AttributeError):
            o.subclassprop

    def test_serialize(self):
        o = self.TestClass(self.data.copy())
        d = o.serializes()
        self.assertEqual(d, '{"id": "abc", "nb": 1, "isBool": true, "created": "2020-11-12", "ts_tz": "2020-10-20T16:40:40.036783+00:00", "ts_iso": "2020-10-20T16:40:40.036783", "ts_notrailingzeros": "2020-10-20T16:40:40.036000"}')

    def test_deser_subclass(self):
        class SubClass(self.TestClass):
            subclassprop: str

        o = SubClass(self.data.copy())
        self.assertEqual(o.id, 'abc')
        self.assertEqual(o.subclassprop, 'subvalue')

