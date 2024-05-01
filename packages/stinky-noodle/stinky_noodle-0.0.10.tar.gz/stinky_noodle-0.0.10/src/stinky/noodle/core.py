import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict

from loguru import logger

from stinky.noodle.utils.enforcer import RuleEnforcer
from stinky.noodle.utils.parser import Parser
from stinky.noodle.utils.ruleset import RuleSetModel


def read_json(path: Path) -> Any:
    with open(path) as fp:
        return json.load(fp)


def try_import_custom_callables(
    mod: str, callables_attr: str = "custom_callables"
) -> Dict:
    """Try to import custom callables by using module and attribute name.

    Args:
        mod (str): The module to import.
        callables_attr (str, optional): The custom callables attribute within above mod.
            Defaults to "custom_callables".

    Returns:
        Dict: A Dictionary of callable names mapped to actual callables.
    """
    try:
        target_module = importlib.import_module(mod)
        return getattr(target_module, callables_attr)
    except ModuleNotFoundError as exception:
        logger.error(f"Unable to import target module {mod}. Maybe a typo?")
        raise exception
    except Exception as exception:
        logger.error(f"Unknown issue occured trying to import {mod}: {str(exception)}")
        raise exception


def entrypoint():
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(prog="noodle")
    parser.add_argument(
        "spec_path",
        help="Path to the spec file",
        default=None,
    )
    parser.add_argument(
        "-c",
        "--ruleset-path",
        help="Path to the ruleset file",
        dest="ruleset_path",
        required=True,
        default=None,
    )

    parser.add_argument(
        "-f",
        "--custom-callables-module",
        help="The custom callables module",
        dest="callables_module",
        required=False,
        default=None,
    )

    parser.add_argument(
        "-d",
        "--custom-callables-dir",
        help="The path that contains the module to be imported",
        dest="callables_dir",
        required=False,
        default=None,
    )

    parser.add_argument(
        "-a",
        "--custom-functions-attr-name",
        help="The name of the attribute within the custom functions module",
        dest="functions_attr_name",
        required=False,
        default="custom_callables",
    )

    args = parser.parse_args()
    ruleset_path = Path(args.ruleset_path).absolute()
    spec_path = Path(args.spec_path).absolute()
    custom_callables_module = args.callables_module
    custom_callables_path = args.callables_dir
    specs = read_json(spec_path)
    ruleset = read_json(ruleset_path)
    ruleset_instance = RuleSetModel(**ruleset)

    custom_callables = {}
    if custom_callables_path is not None:
        sys.path.append(custom_callables_path)
    if custom_callables_module is not None:
        custom_callables = try_import_custom_callables(
            mod=custom_callables_module, callables_attr=args.functions_attr_name
        )

    parser = Parser(specs=specs)

    rule_enforcer = RuleEnforcer(
        ruleset_instance=ruleset_instance,
        spec_parser_instance=parser,
        custom_callables=custom_callables,
    )
    rule_enforcer.enforce()
