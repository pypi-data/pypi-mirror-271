from convert_case import snake_case


def sanitize_callable_name(name: str, custom: bool = False) -> str:
    """Sanitzation for the JS callable name.

    Args:
        name (str): name of the callable
        custom(bool): whether the callable is a custom one

    Returns:
        str: sanitzed python compatible callable name
    """
    prefix = "" if custom else "builtin_"
    return f"{prefix}{snake_case(name)}"
