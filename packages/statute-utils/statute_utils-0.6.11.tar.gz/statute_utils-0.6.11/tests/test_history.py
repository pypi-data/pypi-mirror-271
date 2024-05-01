import pytest
from statute_utils.components.builder import (
    get_last_action,
    get_last_category,
    get_last_cause,
    has_history,
)


@pytest.fixture
def historical():
    return {
        "item": "Section 1",
        "history": [
            {
                "locator": "Section 1",
                "caption": "Courts of justice to be maintained in every province.",
                "statute": "Act No. 136",
            },
            {
                "locator": "Section 1",
                "caption": "Courts Always Open; How Justice Administered.",
                "statute": "1940 Rules of Court",
            },
            {
                "locator": "Section 1",
                "caption": (  # noqa: E501
                    "Courts always open; justice to be promptly and impartially"
                    " administered."
                ),
                "statute": "1964 Rules of Court",
            },
        ],
    }


def test_no_history():
    assert has_history({"item": "Section 1"}) is None


def test_has_history(historical):
    assert has_history(historical) == {
        "locator": "Section 1",
        "caption": (  # noqa: E501
            "Courts always open; justice to be promptly and impartially administered."
        ),
        "statute": "1964 Rules of Court",
    }


def test_get_last_action(historical):
    assert get_last_action(historical) == "Originated"


def test_get_last_category(historical):
    assert get_last_category(historical) == "statute"


def test_get_last_cause(historical):
    assert get_last_cause(historical) == "1964 Rules of Court"
