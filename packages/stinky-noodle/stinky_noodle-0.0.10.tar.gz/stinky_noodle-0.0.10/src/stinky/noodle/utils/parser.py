# from jsonpath_ng.ext import parse
from typing import Any, Dict, List, Union

from pyjsonpath import JsonPath


class Parser:
    def __init__(self, specs: Dict):
        self.specs = specs

    def find_objects(self, json_expr: str) -> Union[List[Any], Dict]:
        """_summary_

        Args:
            json_expr (str): _description_

        Returns:
            Union[List[Any], Dict]: _description_
        """
        return JsonPath(self.specs, json_expr).load()
