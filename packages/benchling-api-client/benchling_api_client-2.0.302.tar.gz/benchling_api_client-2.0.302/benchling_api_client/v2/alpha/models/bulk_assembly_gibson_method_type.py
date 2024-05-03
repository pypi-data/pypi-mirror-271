from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BulkAssemblyGibsonMethodType(Enums.KnownString):
    GIBSON = "GIBSON"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BulkAssemblyGibsonMethodType":
        if not isinstance(val, str):
            raise ValueError(f"Value of BulkAssemblyGibsonMethodType must be a string (encountered: {val})")
        newcls = Enum("BulkAssemblyGibsonMethodType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BulkAssemblyGibsonMethodType, getattr(newcls, "_UNKNOWN"))
