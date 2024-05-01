from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class ThenModel(BaseModel):
    function: str
    field: Optional[str] = None
    functionOptions: Optional[Dict[str, Any]] = {}


class RuleModel(BaseModel):
    description: str
    message: str
    given: List[str]
    message: str
    severity: str
    then: Union[List[ThenModel], ThenModel]


class RuleSetModel(BaseModel):
    description: str
    formats: List[str]
    aliases: Dict[str, str]
    rules: Dict[str, RuleModel]
    functions: List[str]
    functionsDir: str
