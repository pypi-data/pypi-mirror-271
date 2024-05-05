import ddeutil.model.trans as trans
import pytest

from .utils import param


@pytest.mark.parametrize(
    "inputs",
    [
        param({"elements": [1, 2, 3, 4], "do": "foo"}),
        param({"elements": ["1", "2", "3", "4"], "do": "foo"}),
        param({"elements": [{"foo": "bar"}, {"foo": "bar"}], "do": "foo"}),
    ],
)
def test_trans_for_loop(inputs):
    t = trans.ForloopAct(**inputs)
    assert inputs["elements"] == t.elements
    assert inputs["do"] == t.do
