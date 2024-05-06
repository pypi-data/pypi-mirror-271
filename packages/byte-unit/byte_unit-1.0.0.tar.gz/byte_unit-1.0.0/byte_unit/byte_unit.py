from __future__ import annotations

import dataclasses
import re
from enum import Enum
from typing import Tuple, List
from itertools import chain


@dataclasses.dataclass
class Value:
    value: int
    suffixes: List[str]


class ByteUnit(Enum):
    BYTE = Value(1, ["b"])
    KB = Value(1024, ["k", "kb"])
    MB = Value(1024 ** 2, ["m", "mb"])
    GB = Value(1024 ** 3, ["g", "gb"])

    @staticmethod
    def get_all_suffixes() -> List[str]:
        suffixes = map(lambda b: b.value.suffixes, ByteUnit)
        return list(chain.from_iterable(suffixes))

    @staticmethod
    def get_byte_unit_from_suffix(suffix) -> ByteUnit | None:
        unit = list(filter(lambda b: suffix.lower() in b.value.suffixes, ByteUnit))
        return unit[0]


def parse_byte_string(byte_string) -> Tuple[str, ByteUnit]:
    suffixes = "|".join(ByteUnit.get_all_suffixes())
    pattern = re.compile(rf"(^\d+)({suffixes})?$", re.IGNORECASE)
    match = pattern.match(str(byte_string))
    try:
        value, suffix = match.groups()
    except AttributeError as exc:
        raise ValueError(
            "Byte string should be a number followed by any of the suffixes"
            f"{ByteUnit.get_all_suffixes()}") from exc
    unit = ByteUnit.get_byte_unit_from_suffix(suffix) if suffix else ByteUnit.BYTE
    return value, unit


def to_bytes(value: str | int) -> int:
    _value, unit = parse_byte_string(str(value))
    return int(_value) * unit.value.value


def convert_to_unit(value: str | int, to_unit: ByteUnit) -> int:
    _value, _from_unit = parse_byte_string(value)
    if _from_unit.value.value < to_unit.value.value:
        out = int(_value) / int(to_unit.value.value / _from_unit.value.value)
    else:
        out = int(_value) * int(_from_unit.value.value / to_unit.value.value)

    return int(out)
