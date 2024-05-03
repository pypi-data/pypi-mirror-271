from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BulkAssemblySharedAssemblyType(Enums.KnownString):
    CLONING = "CLONING"
    CONCATENATION = "CONCATENATION"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BulkAssemblySharedAssemblyType":
        if not isinstance(val, str):
            raise ValueError(f"Value of BulkAssemblySharedAssemblyType must be a string (encountered: {val})")
        newcls = Enum("BulkAssemblySharedAssemblyType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BulkAssemblySharedAssemblyType, getattr(newcls, "_UNKNOWN"))
