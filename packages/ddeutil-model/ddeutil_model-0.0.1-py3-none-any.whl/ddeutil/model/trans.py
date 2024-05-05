# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from typing import Any, Literal, Optional

from pydantic import (
    BaseModel,
    field_validator,
)


class BaseAct(BaseModel):
    type: str
    desc: Optional[str] = None


class CopyAct(BaseAct):
    type: Literal["copy"] = "copy"
    src: str
    sink: str
    options: dict[str, Any]


class ForloopAct(BaseAct):
    type: Literal["forloop"] = "for"
    elements: list[Any]
    do: str

    @field_validator("elements")
    def elements_validator(cls, values: list[Any]):
        if len(values) > 0:
            _first_element: Any = type(values[0])
            for value in values[1:]:
                if not isinstance(value, _first_element):
                    raise TypeError(
                        "all element in for-loop activity must be the same type"
                    )
        return values


class IfAct(BaseAct):
    type: Literal["if"] = "if"
    condition: str
    left: str
    right: str


class SensorAct(BaseAct):
    type: Literal["sensor"] = "sensor"
    condition: str


class HookAct(BaseAct):
    type: Literal["hook"] = "hook"
    hook: str
