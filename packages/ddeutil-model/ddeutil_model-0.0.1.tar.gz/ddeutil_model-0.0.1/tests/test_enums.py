from ddeutil.model.__enums import Loading, Status


def test_status_failed():
    e: Status = Status.FAILED

    assert e == Status.FAILED
    assert e in Status
    assert e <= Status.FAILED
    assert e < Status.WAITING
    assert e > Status.SUCCESS
    assert e.value == 1
    assert not e.in_process()


def test_loading():
    e: Loading = Loading.FULL_DUMP

    assert e == Loading.FULL_DUMP
    assert e != Loading.DELTA
    assert e.value == "F"
