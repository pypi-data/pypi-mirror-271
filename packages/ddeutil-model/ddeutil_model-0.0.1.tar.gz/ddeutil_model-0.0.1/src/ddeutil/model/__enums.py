# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from enum import Enum, IntEnum
from functools import total_ordering


def enum_ordering(cls):
    """Add order property to Enum object."""

    def __lt__(self, other):
        if type(other) is type(self):
            return self.value < other.value
        raise ValueError("Cannot compare different Enums")

    cls.__lt__ = __lt__
    return total_ordering(cls)


class StrEnum(str, Enum):
    """
    StrEnum where enum.auto() returns the field name.
    See https://docs.python.org/3.9/library/enum.html#using-automatic-values
    """

    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: list,
    ) -> str:
        return name

    def __str__(self) -> str:
        return self.value


@enum_ordering
class Status(IntEnum):
    SUCCESS: int = 0
    APPROVED: int = 0
    FAILED: int = 1
    WAITING: int = 2
    PROCESSING: int = 2
    TRIGGERED: int = 2

    def in_process(self) -> bool:
        return self.value == 2


class Loading(StrEnum):
    FULL_DUMP = "F"
    DELTA = "D"
    MERGE = "D"
    TRANSACTION = "T"
    SCD_DELTA = "SCD_D"
    SCD_DUMP = "SCD_F"
    SCD_TRANS = "SCD_T"


class DataLayer(IntEnum):
    RAW: int = 0
    STAGING: int = 1
    PERSISTED: int = 2
    CURATED: int = 3
    MART: int = 4
