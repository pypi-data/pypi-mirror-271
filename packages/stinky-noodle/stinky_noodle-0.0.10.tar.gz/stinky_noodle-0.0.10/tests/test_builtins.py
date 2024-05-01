from typing import Any, Dict, List, Optional, Set, Tuple, Union

import pytest

from stinky.noodle.utils.builtins import (
    builtin_alphabetical,
    builtin_casing,
    builtin_enumeration,
    builtin_falsy,
    builtin_length,
    builtin_pattern,
    builtin_schema,
)


@pytest.mark.parametrize(
    ("input_obj", "keyed_by", "result"),
    [
        (["a", "c", "b"], None, False),
        (["a", "b", "c"], None, True),
        (
            [
                {"key": 1, "val": "a"},
                {"key": 3, "val": "c"},
                {"key": 2, "val": "b"},
            ],
            "key",
            False,
        ),
        (
            [
                {"key": 1, "val": "a"},
                {"key": 3, "val": "b"},
                {"key": 2, "val": "c"},
            ],
            "val",
            True,
        ),
    ],
)
def test_builtin_alphabetical(input_obj: Any, keyed_by: Optional[str], result: bool):
    """Test the alphabetical builtin"""
    assert builtin_alphabetical(obj=input_obj, keyed_by=keyed_by) is result


@pytest.mark.parametrize(
    ("obj", "values", "result"),
    [
        (
            "a",
            (
                "a",
                "b",
            ),
            True,
        ),
        (
            "c",
            (
                "a",
                "b",
            ),
            False,
        ),
        (
            "a",
            {
                "a",
                "b",
            },
            True,
        ),
        (
            "c",
            {
                "a",
                "b",
            },
            False,
        ),
        ("a", [], False),
        ("c", [], False),
    ],
)
def test_builtin_enumeration(obj: Any, values: Union[Set, List, Tuple], result: bool):
    """Test the enumeration builtin"""
    assert builtin_enumeration(obj=obj, values=values) is result


@pytest.mark.parametrize(
    ("obj", "result"),
    [
        (False, True),
        (0, True),
        (1, False),
        ("anything", False),
    ],
)
def test_builtin_falsy(obj: Any, result: bool):
    """Test the falsy builtin"""
    assert builtin_falsy(obj=obj) is result


@pytest.mark.parametrize(
    ("obj", "min_arg", "max_arg", "result"),
    [
        ("", 0, 0, False),
        ("", 0, 1, True),
        ("", 2, 4, False),
        ("a", 0, 1, False),
        ("a", 1, 2, True),
    ],
)
def test_builtin_length(obj: Any, min_arg: int, max_arg: int, result: bool):
    """Test the length builtin"""
    assert builtin_length(obj=obj, min=min_arg, max=max_arg) is result


@pytest.mark.parametrize(
    ("obj", "match", "not_match", "result"),
    [
        ("some value", ".*(value)$", None, True),
        ("some value", "^(value).*", None, False),
        ("some value", None, ".*(value)$", False),
        ("some value", None, "^(value).*", True),
    ],
)
def test_builtin_pattern(
    obj: Any, match: Optional[str], not_match: Optional[str], result: bool
):
    """Test the pattern builtin"""
    assert builtin_pattern(obj=obj, match=match, not_match=not_match) is result


@pytest.mark.parametrize(
    ("obj", "type", "disallow_digits", "separator", "result"),
    [
        # {"char": "", "allow_leading": True}
        ("supposedToBeCamelCase", "camel", False, None, True),
        ("SupposedToBePascalCase", "pascal", False, None, True),
        ("NotSupposedToBeCamelCase", "camel", False, None, False),
        ("supposed_to_be_snake_case", "snake", False, None, True),
        ("not_supposed_to_be_Snake_case", "snake", False, None, False),
        ("supposed-to-be-kebab-case", "kebab", False, None, True),
        ("not_supposed-to-be-kebab-case", "kebab", False, None, False),
        ("SUPPOSED-TO-BE-COBOL-CASE", "cobol", False, None, True),
        ("NOT_SUPPOSED-TO-BE-COBOL-CASE", "cobol", False, None, False),
        ("SUPPOSED_TO_BE_MACRO_CASE", "macro", False, None, True),
        (
            "#SUPPOSED#TO#BE#MACRO#CASE",
            "macro",
            False,
            {"allow_leading": True, "char": "#"},
            True,
        ),
        (
            "#SUPPOSED#TO#BE#MACRO#CASE",
            "macro",
            False,
            {"allow_leading": False, "char": "#"},
            False,
        ),
        (
            "SUPPOSED!TO!BE!MACRO!CASE",
            "macro",
            False,
            {"allow_leading": False, "char": "!"},
            True,
        ),
        ("NOT-SUPPOSED_TO_BE_MACRO_CASE", "macro", False, None, False),
        ("not-supposed-to-be-macro-case", "macro", False, None, False),
        ("supposedtobeflatcase", "flat", False, None, True),
        ("NOTsupposedtobeflatcase", "flat", False, None, False),
        ("not-supposedtobeflatcase", "flat", False, None, False),
    ],
)
def test_builtin_casing(
    obj: str, type: str, disallow_digits: bool, separator: Optional[Dict], result: bool
):
    """Test the casing builtin"""
    assert (
        builtin_casing(
            obj=obj, type=type, disallow_digits=disallow_digits, separator=separator
        )
        is result
    )


@pytest.mark.parametrize(
    ("obj", "schema", "dialect", "all_errors", "expected_errors"),
    [
        (
            [{}, 4, "bla"],
            {
                "items": {
                    "anyOf": [
                        {"type": "string", "maxLength": 2},
                        {"type": "integer", "minimum": 5},
                    ]
                }
            },
            "draft202012",
            True,
            [
                [
                    [0, "type"],
                    "{} is not of type 'string'",
                    [1, "type"],
                    "{} is not of type 'integer'",
                ],
                [
                    [0, "type"],
                    "4 is not of type 'string'",
                    [1, "minimum"],
                    "4 is less than the minimum of 5",
                ],
                [
                    [0, "maxLength"],
                    "'bla' is too long",
                    [1, "type"],
                    "'bla' is not of type 'integer'",
                ],
            ],
        ),
        (
            [{}, 4, "bla"],
            {
                "items": {
                    "anyOf": [
                        {"type": "string", "maxLength": 2},
                        {"type": "integer", "minimum": 5},
                    ]
                }
            },
            "draft202012",
            False,
            [
                [
                    [0, "type"],
                    "{} is not of type 'string'",
                ],
                [
                    [0, "type"],
                    "4 is not of type 'string'",
                ],
                [
                    [0, "maxLength"],
                    "'bla' is too long",
                ],
            ],
        ),
    ],
)
def test_builtin_schema(
    obj: Any,
    schema: Dict,
    dialect: Optional[str],
    all_errors: bool,
    expected_errors: List[Any],
):
    """Test the schema builtin"""
    assert (
        builtin_schema(obj=obj, schema=schema, dialect=dialect, all_errors=all_errors)
        == expected_errors
    )


# @pytest.mark.parametrize(
#     ("obj", "result"),
#     [
#     ],
# )
# def test_builtin_unreferenced_reusable_object(obj: Any, result: bool):
#     """Test the truthy builtin"""
#     assert builtin_truthy(obj=obj) is result
