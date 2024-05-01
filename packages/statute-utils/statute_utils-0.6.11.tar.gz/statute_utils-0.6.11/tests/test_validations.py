from statute_utils import STYLES_NAMED, STYLES_SERIAL, get_local_statute_db


def test_named_collection():
    for named in STYLES_NAMED:
        if named.matches:
            for sample in named.matches:
                assert named.pattern.fullmatch(sample)


def test_serial_collection():
    for serial in STYLES_SERIAL:
        if serial.matches:
            for sample in serial.matches:
                assert serial.pattern.fullmatch(sample)


def test_named_and_dated_collection():
    for named in STYLES_NAMED:
        if named.options:
            for option in named.options:
                if get_local_statute_db():
                    assert option.date
