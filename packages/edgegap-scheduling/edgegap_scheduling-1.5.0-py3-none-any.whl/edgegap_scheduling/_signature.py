import inspect
import logging
from types import GeneratorType
from typing import Any, Callable

from pydantic import BaseModel

from ._depends import Depends


class TaskSignature:
    def __init__(self, identifier: str, name: str, func: Callable):
        self.__identifier = identifier
        self.__name = name
        self.__func = func

    def get_arguments(
        self,
        parameters: BaseModel | type[BaseModel] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        specs = {}
        generators = {}
        signature = inspect.signature(self.__func)

        for name, param in signature.parameters.items():
            match param.annotation:
                case logging.Logger:
                    specs[name] = logging.getLogger(f'scheduling.{self.__identifier}')
                case parameters.__class__:
                    specs[name] = parameters
                case parameters:
                    specs[name] = parameters()

            match param.default:
                case Depends():
                    value = param.default.dependency()

                    if isinstance(value, GeneratorType):
                        generators[name] = value
                    else:
                        specs[name] = value

        return specs, generators
