from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BulkAssemblyGoldenGateMethodType(Enums.KnownString):
    GOLDEN_GATE = "GOLDEN_GATE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BulkAssemblyGoldenGateMethodType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BulkAssemblyGoldenGateMethodType must be a string (encountered: {val})"
            )
        newcls = Enum("BulkAssemblyGoldenGateMethodType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BulkAssemblyGoldenGateMethodType, getattr(newcls, "_UNKNOWN"))
