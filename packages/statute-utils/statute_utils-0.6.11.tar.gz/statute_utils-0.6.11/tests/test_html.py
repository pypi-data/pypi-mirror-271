import json

import pytest
from statute_utils.components import make_branch, make_branch_json_array, md_to_html


@pytest.fixture
def construct_statute_mp_sql_without_build_branch_func():
    return [
        {
            "item": "Canon I",
            "caption": "Independence",
            "content": (
                "The independence of a lawyer in the discharge of professional duties"
                " without any improper influence, restriction, pressure, or"
                " interference, direct or indirect, ensures effective legal"
                " representation and is ultimately imperative for the rule of law. (n)"
            ),
            "id": "1.2.",
        },
        {
            "item": "Section 5",
            "caption": "Lawyer's duty and discretion in procedure and strategy.",
            "id": "1.2.5.",
            "units": [
                {
                    "item": "Paragraph 1",
                    "content": (
                        "A lawyer shall not allow the client to dictate or determine"
                        " the procedure in handling the case. (19.03a)"
                    ),
                    "id": "1.2.5.1.",
                },
                {
                    "item": "Paragraph 2",
                    "content": (
                        "Nevertheless, a lawyer shall respect the client's decision to"
                        " settle or compromise the case after explaining its"
                        " consequences to the client. (n)"
                    ),
                    "id": "1.2.5.2.",
                },
            ],
        },
    ]


@pytest.fixture
def single_subtree_result():
    return {
        "units": [
            {
                "item": "Canon I",
                "caption": "Independence",
                "content": (
                    "The independence of a lawyer in the discharge of professional"
                    " duties without any improper influence, restriction, pressure, or"
                    " interference, direct or indirect, ensures effective legal"
                    " representation and is ultimately imperative for the rule of"
                    " law. (n)"
                ),
                "id": "1.2.",
                "units": [
                    {
                        "item": "Section 5",
                        "caption": (
                            "Lawyer's duty and discretion in procedure and strategy."
                        ),
                        "id": "1.2.5.",
                        "units": [
                            {
                                "item": "Paragraph 1",
                                "content": (
                                    "A lawyer shall not allow the client to dictate or"
                                    " determine the procedure in handling the case."
                                    " (19.03a)"
                                ),
                                "id": "1.2.5.1.",
                            },
                            {
                                "item": "Paragraph 2",
                                "content": (
                                    "Nevertheless, a lawyer shall respect the client's"
                                    " decision to settle or compromise the case after"
                                    " explaining its consequences to the client. (n)"
                                ),
                                "id": "1.2.5.2.",
                            },
                        ],
                    }
                ],
            }
        ]
    }


def test_subtree(
    construct_statute_mp_sql_without_build_branch_func, single_subtree_result
):
    assert single_subtree_result == make_branch(
        {}, construct_statute_mp_sql_without_build_branch_func
    )


def test_build_branch(construct_statute_mp_sql_without_build_branch_func):
    assert (
        '{"item": "Canon I", "caption": "Independence", "content": "The independence of'
        " a lawyer in the discharge of professional duties without any improper"
        " influence, restriction, pressure, or interference, direct or indirect,"
        " ensures effective legal representation and is ultimately imperative for the"
        ' rule of law. (n)", "id": "1.2.", "units": [{"item": "Section 5", "caption":'
        ' "Lawyer\'s duty and discretion in procedure and strategy.", "id": "1.2.5.",'
        ' "units": [{"item": "Paragraph 1", "content": "A lawyer shall not allow the'
        ' client to dictate or determine the procedure in handling the case. (19.03a)",'
        ' "id": "1.2.5.1."}, {"item": "Paragraph 2", "content": "Nevertheless, a lawyer'
        " shall respect the client's decision to settle or compromise the case after"
        ' explaining its consequences to the client. (n)", "id": "1.2.5.2."}]}]}'
        == make_branch_json_array(
            json.dumps(construct_statute_mp_sql_without_build_branch_func)
        )
    )
