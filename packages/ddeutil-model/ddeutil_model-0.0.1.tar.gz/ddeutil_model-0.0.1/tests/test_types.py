import unittest

import ddeutil.model.__types as tp


class TestTypes(unittest.TestCase):

    def test_db_url(self):
        t = tp.CustomUrl(url="driver://name:pass@host:1234")
        self.assertEqual("driver", t.scheme)
        self.assertEqual("name", t.username)
        self.assertEqual("pass", t.password)
        self.assertEqual("host", t.host)
        self.assertEqual(1234, t.port)
        self.assertDictEqual({}, dict(t.query_params()))
