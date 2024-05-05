import unittest

import ddeutil.model.dtype as dtype


class TestCharType(unittest.TestCase):
    def test_char_init(self):
        t = dtype.CharType(type="char")
        self.assertEqual("char", t.type)
        self.assertEqual(-1, t.max_length)

        t = dtype.CharType(type="char", max_length=1000)
        self.assertEqual("char", t.type)
        self.assertEqual(1000, t.max_length)

    def test_char_model_validate(self):
        t = dtype.CharType.model_validate({"type": "char", "max_length": 1000})
        self.assertEqual("char", t.type)
        self.assertEqual(1000, t.max_length)


class TestVarcharType(unittest.TestCase):
    def test_varchar_init(self):
        t = dtype.VarcharType(type="varchar")
        self.assertEqual("varchar", t.type)
        self.assertEqual(-1, t.max_length)

        t = dtype.VarcharType(type="varchar", max_length=1000)
        self.assertEqual("varchar", t.type)
        self.assertEqual(1000, t.max_length)

        t = dtype.VarcharType(type="varchar", max_length="1000")
        self.assertEqual("varchar", t.type)
        self.assertEqual(1000, t.max_length)

    def test_varchar_model_validate(self):
        t = dtype.VarcharType.model_validate(
            {"type": "varchar", "max_length": 1000}
        )
        self.assertEqual("varchar", t.type)
        self.assertEqual(1000, t.max_length)

        t = dtype.VarcharType.model_validate(
            {"type": "varchar", "max_length": "1000"}
        )
        self.assertEqual("varchar", t.type)
        self.assertEqual(1000, t.max_length)


class TestIntegerType(unittest.TestCase):
    def test_int_init(self):
        t = dtype.IntegerType(type="int")
        self.assertEqual("integer", t.type)
