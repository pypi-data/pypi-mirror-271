from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BulkAssemblyCreatedPrimerType(Enums.KnownString):
    BULK_ASSEMBLY_CREATED_PRIMER = "BULK_ASSEMBLY_CREATED_PRIMER"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BulkAssemblyCreatedPrimerType":
        if not isinstance(val, str):
            raise ValueError(f"Value of BulkAssemblyCreatedPrimerType must be a string (encountered: {val})")
        newcls = Enum("BulkAssemblyCreatedPrimerType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BulkAssemblyCreatedPrimerType, getattr(newcls, "_UNKNOWN"))
