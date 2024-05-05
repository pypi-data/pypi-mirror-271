import unittest

import ddeutil.model.conn as conn


class TestDBConn(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_db_conn_from_url(self):
        t = conn.DbConn.from_url(
            url=(
                "postgres+psycopg://demo:P@ssw0rd@localhost:5432/db"
                "?echo=True&timeout=10"
            )
        )
        self.assertEqual("postgres+psycopg", t.driver)

        t = conn.DbConn.from_url(
            url="mssql://demo:P@ssw0rd@127.0.0.1:5432/postgres"
        )
        self.assertEqual("mssql", t.driver)
        self.assertEqual("127.0.0.1", t.host)
        self.assertEqual("P%40ssw0rd", t.pwd.get_secret_value())


class TestFlConn(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_fl_conn_from_url(self):
        t = conn.FlConn.from_url(
            url="sqlite:///D:/data/warehouse/main.sqlite?echo=True"
        )
        self.assertEqual("sqlite", t.sys)
        self.assertEqual("/D:/data/warehouse/main.sqlite", t.path)
        self.assertDictEqual({"echo": "True"}, t.options)
