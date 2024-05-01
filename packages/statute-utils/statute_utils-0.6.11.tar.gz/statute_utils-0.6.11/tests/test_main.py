from dataclasses import asdict

import pytest
from statute_utils import extract_named_rules, extract_rules, extract_serial_rules


@pytest.mark.parametrize(
    "text, extracted",
    [
        (
            "Veto Message - 11534",
            [
                {"cat": "veto", "num": "11534"},
            ],
        ),
        (
            "Republic Act No. 386, 1114, and 11000-",
            [
                {"cat": "ra", "num": "386"},
                {"cat": "ra", "num": "1114"},
                {"cat": "ra", "num": "11000"},
            ],
        ),
        (
            (  # noqa: E501
                "The Civil Code of the Philippines, the old Spanish Civil"
                " Code; Rep Act No. 386"
            ),
            [
                {"cat": "ra", "num": "386"},
                {"cat": "ra", "num": "386"},
                {"cat": "spain", "num": "civil"},
            ],
        ),
    ],
)
def test_extract_rules(text, extracted):
    assert list(asdict(i) for i in extract_rules(text)) == extracted


@pytest.mark.parametrize(
    "text, result",
    [
        (
            "This is the 1987 PHIL CONST; hello world, the Spanish Penal Code.",
            [
                {"cat": "const", "num": "1987"},
                {"cat": "spain", "num": "penal"},
            ],
        ),
    ],
)
def test_extract_rules_named(text, result):
    assert list(asdict(i) for i in extract_named_rules(text)) == result


@pytest.mark.parametrize(
    "text, result",
    [
        (
            (  # noqa: E501
                "A.M. No. 02-11-10-SC or the Rules on Declaration of Absolute;"
                " Administrative Order No. 3 by enacting A.M. No. 99-10-05-0;"
                " Parenthetically, under these statutes [referring to RA Nos."
                " 965 and 2630], Commonwealth Act (C.A.) No. 613, otherwise"
                " known as the <em>Philippine Immigration Act of 1940</em>"
            ),
            [
                {"cat": "rule_am", "num": "02-11-10-sc"},
                {"cat": "rule_am", "num": "99-10-05-0"},
                {"cat": "ra", "num": "965"},
                {"cat": "ra", "num": "2630"},
                {"cat": "ca", "num": "613"},
            ],
        ),
        (
            (  # noqa: E501
                "There is no question that Section 2 of Presidential Decree"
                " No. 1474 is inconsistent with Section 62 of Republic Act No."
                " 3844.; Petitioner’s case was decided under P.D. No. 971, as"
                " amended by P.D. No. 1707."
            ),
            [
                {"cat": "pd", "num": "1474"},
                {"cat": "ra", "num": "3844"},
                {"cat": "pd", "num": "971"},
                {"cat": "pd", "num": "1707"},
            ],
        ),
        (
            (  # noqa: E501
                "Nonetheless, the Court has acknowledged the practical value"
                " of the process of marking the confiscated contraband and"
                " considered it as an initial stage in the chain of custody -"
                " a process preliminary and preparatory to the physical"
                " inventory and photograph requirements in Section 21 of"
                " Republic Act No. 9165:"
            ),
            [{"cat": "ra", "num": "9165"}],
        ),
        (
            (  # noqa: E501
                "As amended by Republic Act No. 9337- An Act Amending Sections"
                " 27, 28, 34, 106, 107, 108, 109, 110, 111, 112, 113, 114,"
                " 116, 117, 119, 121, 148, 151, 236, 237 and 288 of the"
                " National Internal Revenue Code of 1997"
            ),
            [{"cat": "ra", "num": "9337"}],
        ),
    ],
)
def test_rule_find_all(text, result):
    assert list(asdict(i) for i in extract_serial_rules(text)) == result
