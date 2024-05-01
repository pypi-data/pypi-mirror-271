import re
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from jsonschema.validators import (
    Draft3Validator,
    Draft4Validator,
    Draft6Validator,
    Draft7Validator,
    Draft201909Validator,
    Draft202012Validator,
)

FALSY = (False, "", 0, None)
CASE_PATTERNS = {
    # "<type>": ("<patt>", "<default_separator>")
    "camel": ("^{0:s}[a-z]+({1:s}[A-Z][a-z]+)+$", ""),
    "pascal": ("^{0:s}[A-Z][a-z]+({1:s}[A-Z][a-z]+)+$", ""),
    "snake": ("^{0:s}[a-z]+({1:s}[a-z]+)+$", "_"),
    "kebab": ("^{0:s}[a-z]+({1:s}[a-z]+)+$", "-"),
    "cobol": ("^{0:s}[A-Z]+({1:s}[A-Z]+)+$", "-"),
    "macro": ("^{0:s}[A-Z]+({1:s}[A-Z]+)+$", "_"),
    "flat": ("^{0:s}[a-z{1:s}]+$", ""),
}

JSON_SCHEMA_VALIDATORS = {
    "draft3": Draft3Validator,
    "draft4": Draft4Validator,
    "draft6": Draft6Validator,
    "draft7": Draft7Validator,
    "draft201909": Draft201909Validator,
    "draft202012": Draft202012Validator,
}


def builtin_alphabetical(obj: Any, keyed_by: Optional[str] = None) -> bool:
    """Check if obj is sorted, optionally by key

    Args:
        obj (Any): The obj to verify
        keyed_by (Optional[str], optional): key to use for sorting. Defaults to None.

    Raises:
        ValueError: Raised when the specified `key` does not exist in `obj`

    Returns:
        bool: Indicates whether `obj` is sorted alphabetically or not.
    """
    if obj is None:
        raise ValueError("obj cannot have value None")

    if keyed_by is not None:
        return sorted(obj, key=lambda obj: obj[keyed_by]) == obj

    return sorted(obj) == obj


def builtin_enumeration(obj: Any, values: Union[Set, List, Tuple], **kwargs) -> bool:
    """Check for presence in predefined list.

    Args:
        obj (Any): The obj to verify

    Returns:
        bool: Indicates wheter `obj` is equal to one of `values`.
    """
    if obj is None:
        raise ValueError("obj cannot have value None")

    return obj in values


def builtin_falsy(obj: Any, **kwargs) -> bool:
    """Check for falsiness

    Args:
        obj (Any): The obj to verify

    Returns:
        bool: Indicates wheter `obj` is equal to one of the falsy values.
    """
    return obj in FALSY


def builtin_length(obj: Any, min: int, max: int) -> bool:
    """Check min-max bounds of obj

    Args:
        obj (Any): The obj to verify
        min (int): Minimum (inclusive)
        max (int): Maximum (non-inclusive)

    Raises:
        ValueError: raised when obj is None

    Returns:
        bool: Whether `obj` is within the required bounds (`min` <= `obj` < `max`)
    """
    if obj is None:
        raise ValueError("obj cannot have value None")

    return min <= len(obj) < max


def builtin_pattern(
    obj: str, match: Optional[str] = None, not_match: Optional[str] = None
) -> bool:
    """Apply a regex pattern or negated regex pattern to a string input.

    Args:
        obj (Any): The object we're applying the matching on.
        match (Optional[str], optional): Pattern we want to find a match for.
            Defaults to None.
        not_match (Optional[str], optional): Pattern we don't want to find a
            math for. Defaults to None.

    Returns:
        bool: Whether we matched what was specified in `match` or
            we didn't match what was in `not_match`.
    """
    if obj is None:
        raise ValueError("obj cannot have value None")

    cond = True
    if match is not None:
        cond &= re.match(match, obj) is not None
    if not_match is not None:
        cond &= not (re.match(not_match, obj) is not None)
    return cond


def builtin_casing(
    obj: str,
    type: str,
    disallow_digits: Optional[bool] = False,
    separator: Optional[Dict] = None,
) -> bool:
    """Detect the use of different casings.

    Args:
        obj (Any): The object we're applying the matching on.
        type (str): Type of casing.
        disallow_digits (Optional[bool], optional): Whether digits are allowed at all.
            Defaults to False.
        separator (Optional[Dict], optional): a dict containing
            char (str) and allow_leading (bool). Defaults to None.
    """

    if obj is None:
        raise ValueError("obj cannot have value None")

    if disallow_digits and re.match(r"[0-9]", obj):
        return False

    try:
        patt, sep = CASE_PATTERNS[type]
    except KeyError:
        raise ValueError(f"Case type {type} is not recognized.")

    leading_sep = ""
    if separator is not None:
        sep = re.escape(separator.get("char", sep))
        leading = separator.get("allow_leading", False)
        if leading:
            leading_sep = sep

    patt = patt.format(leading_sep, sep)
    return re.match(patt, obj) is not None


def builtin_schema(
    obj: Any, schema: Dict, dialect: str, all_errors: Optional[bool] = False
) -> List[str]:
    """Verify json schema instance represented by obj.

    Args:
        obj (Any): The instance
        schema (Dict): The json schema
        dialect (str): the json schema dialect
        all_errors (Optional[bool], optional): whether to return errors
            of the first found type only, or to return all. Defaults to False.

    Raises:
        ValueError: Raised when `obj` is None
        ValueError: Raised of the json schema `dialect` is invalid

    Returns:
        List[str]: Nested list of json schema validation errors
    """
    if obj is None:
        raise ValueError("obj cannot have value None")

    try:
        validator_cls = JSON_SCHEMA_VALIDATORS[dialect]
    except KeyError:
        raise ValueError(
            f"Dialect {dialect} is not valid, choose one of ({', '.join(JSON_SCHEMA_VALIDATORS)})"
        )
    validator = validator_cls(schema=schema)
    errors = sorted(validator.iter_errors(obj), key=lambda e: e.path)
    out = []
    for error in errors:
        temp = []
        for suberror in sorted(error.context, key=lambda e: e.schema_path):
            temp += [list(suberror.schema_path), suberror.message]
            if not all_errors:
                break
        out += [temp]
    return out


def builtin_truthy(obj: Any, **kwargs) -> bool:  # pragma: no cover
    """Check for non-falsiness

    Args:
        obj (Any): The obj to verify

    Returns:
        bool: Indicates whether `obj` is not falsy
    """
    return not builtin_falsy(obj)


def builtin_undefined(obj: Any) -> bool:  # pragma: no cover
    """Check for None values

    Args:
        obj (Any): The obj to verify

    Returns:
        bool: Indicates whether `obj` is None
    """
    return obj is None


def builtin_defined(obj: Any) -> bool:  # pragma: no cover
    """Check for non-None values

    Args:
        obj (Any): The obj to verify

    Returns:
        bool: Indicates whether `obj` is not None
    """
    return not builtin_undefined(obj)


def builtin_unreferenced_reusable_object(obj: Any):  # pragma: no cover
    # TODO: implementation
    pass


def builtin_xor(obj: Any, properties: List[str]) -> bool:
    """Check for exclusive-or existence of properties in obj.

    Args:
        obj (Any): The obj to verify
        properties (List[str]): List of properties that should exist exclusively.

    Returns:
        bool: Whether or not only one of `properties` is defined.
    """
    return len(builtin_defined(obj.get(prop) for prop in properties)) == 1
