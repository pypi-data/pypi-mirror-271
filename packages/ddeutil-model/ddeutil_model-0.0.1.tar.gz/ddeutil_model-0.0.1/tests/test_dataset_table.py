import unittest

import ddeutil.model.datasets.db as db


class TestBaseTable(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_base_table_init(self):
        t = db.BaseTbl(
            name="foo",
            feature=[db.Col(name="foo", dtype="varchar( 10 )")],
        )
        self.assertListEqual(
            t.feature,
            [db.Col(name="foo", dtype="varchar( 10 )")],
        )


class TestTable(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_table_init(self):
        t = db.Tbl(
            name="foo",
            feature=[db.Col(name="foo", dtype="varchar( 10 )")],
        )
        self.assertListEqual(
            t.feature,
            [db.Col(name="foo", dtype="varchar( 10 )")],
        )
        self.assertEqual(t.pk, db.Pk(of="foo"))
        self.assertListEqual(t.fk, [])

        t = db.Tbl(
            name="foo", feature=[{"name": "foo", "dtype": "varchar( 100 )"}]
        )
        self.assertDictEqual(
            t.model_dump(by_alias=False),
            {
                "name": "foo",
                "feature": [
                    {
                        "check": None,
                        "default": None,
                        "dtype": {"max_length": 100, "type": "varchar"},
                        "fk": {},
                        "name": "foo",
                        "nullable": True,
                        "pk": False,
                        "unique": False,
                    }
                ],
                "pk": {"cols": [], "of": "foo"},
                "fk": [],
            },
        )

        t = db.Tbl(
            name="foo",
            feature=[{"name": "foo", "dtype": "varchar( 100 ) primary key"}],
        )
        self.assertDictEqual(
            t.model_dump(by_alias=False),
            {
                "name": "foo",
                "feature": [
                    {
                        "check": None,
                        "default": None,
                        "dtype": {"max_length": 100, "type": "varchar"},
                        "fk": {},
                        "name": "foo",
                        "nullable": False,
                        "pk": True,
                        "unique": False,
                    }
                ],
                "pk": {"cols": ["foo"], "of": "foo"},
                "fk": [],
            },
        )

    def test_table_init_with_pk(self):
        t = db.Tbl(
            name="foo",
            feature=[{"name": "id", "dtype": "integer", "pk": True}],
        )
        self.assertDictEqual(
            t.model_dump(by_alias=False),
            {
                "name": "foo",
                "feature": [
                    {
                        "check": None,
                        "default": None,
                        "dtype": {"type": "integer"},
                        "fk": {},
                        "name": "id",
                        "nullable": False,
                        "pk": True,
                        "unique": False,
                    }
                ],
                "pk": {"cols": ["id"], "of": "foo"},
                "fk": [],
            },
        )

    def test_table_model_validate(self):
        t = db.Tbl.model_validate(
            {
                "name": "foo",
                "feature": [
                    {"name": "id", "dtype": "integer", "pk": True},
                    {
                        "name": "name",
                        "dtype": "varchar( 256 )",
                        "nullable": False,
                    },
                ],
            },
        )
        self.assertDictEqual(
            t.model_dump(by_alias=False),
            {
                "name": "foo",
                "feature": [
                    {
                        "check": None,
                        "default": None,
                        "dtype": {"type": "integer"},
                        "fk": {},
                        "name": "id",
                        "nullable": False,
                        "pk": True,
                        "unique": False,
                    },
                    {
                        "check": None,
                        "default": None,
                        "dtype": {"type": "varchar", "max_length": 256},
                        "fk": {},
                        "name": "name",
                        "nullable": False,
                        "pk": False,
                        "unique": False,
                    },
                ],
                "pk": {"cols": ["id"], "of": "foo"},
                "fk": [],
            },
        )
