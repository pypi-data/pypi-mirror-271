from typing import Callable, List, Optional

from loguru import logger

from stinky.noodle.utils import builtins, sanitize_callable_name
from stinky.noodle.utils.exceptions import NonExistentCallableError
from stinky.noodle.utils.parser import Parser
from stinky.noodle.utils.ruleset import RuleSetModel


class RuleEnforcer:
    def __init__(
        self,
        ruleset_instance: RuleSetModel,
        spec_parser_instance: Parser,
        custom_callables: Optional[List[Callable]] = [],
    ):
        self.custom_callables = custom_callables
        self.ruleset_instance = ruleset_instance
        self.spec_parser_instance = spec_parser_instance

    def get_callable(self, callable_name: str) -> Callable:
        """Get callable by string name.

        Args:
            callable_name (str): Name of the callable attribute.

        Returns:
            Callable: The callable.
        """
        sanitized_callable_name = sanitize_callable_name(callable_name)
        try:
            callable = getattr(builtins, sanitized_callable_name)
            return callable
        except AttributeError:
            logger.debug(
                f"Callabel with name: {callable_name} is not a built-in. Trying custom callables."
            )

        sanitized_callable_name = sanitize_callable_name(callable_name, custom=True)
        try:
            callable = self.custom_callables[sanitized_callable_name]
        except KeyError:
            logger.debug(
                f'Callabel with name: "{callable_name}" is not a custom callable either.'
            )
            raise NonExistentCallableError(
                f'Callable "{callable_name}" does not exist.'
            )

        return callable

    def enforce(self):
        validation_fail_count = 0
        for rule_name, rule_instance in self.ruleset_instance.rules.items():
            logger.info(f"Working on rule with name: {rule_name}.")
            for given_path in rule_instance.given:
                matches = self.spec_parser_instance.find_objects(given_path)
                then = rule_instance.then
                if not isinstance(rule_instance.then, list):
                    then = [rule_instance.then]
                for then_case in then:
                    callable = self.get_callable(then_case.function)
                    func_ops = then_case.functionOptions

                    for match in matches:
                        obj = match

                        if then_case.field is not None:
                            obj = match.get(then_case.field)
                            result = callable(obj=obj, **func_ops)

                            if not result:
                                validation_fail_count += 1
                                logger.error(
                                    f'Validation on given "{given_path}" with func "{then_case.function}" failed.'
                                )

                            else:
                                logger.success(
                                    f'Validation on given "{given_path}" with func "{then_case.function}" succeeded.'
                                )
        if validation_fail_count == 0:
            logger.success("[Linting finished] Validation succeeded. No issues found.")
        elif validation_fail_count > 0:
            logger.error(
                f"[Linting finished] Validation did not succeed, found {validation_fail_count} issues."
            )
