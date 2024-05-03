from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BulkAssemblyConstantBinBinType(Enums.KnownString):
    CONSTANT = "CONSTANT"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BulkAssemblyConstantBinBinType":
        if not isinstance(val, str):
            raise ValueError(f"Value of BulkAssemblyConstantBinBinType must be a string (encountered: {val})")
        newcls = Enum("BulkAssemblyConstantBinBinType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BulkAssemblyConstantBinBinType, getattr(newcls, "_UNKNOWN"))
