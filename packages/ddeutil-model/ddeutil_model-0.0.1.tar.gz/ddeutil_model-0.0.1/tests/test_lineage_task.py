import unittest

import ddeutil.model.lineage as lineages
from ddeutil.model.__enums import Status


class TestBaseTask(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_base_task_init(self):
        t = lineages.BaseTask(st=Status.WAITING)
        print(t.model_dump())
