from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BulkAssemblyConcatenationMethodType(Enums.KnownString):
    CONCATENATION = "CONCATENATION"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BulkAssemblyConcatenationMethodType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BulkAssemblyConcatenationMethodType must be a string (encountered: {val})"
            )
        newcls = Enum("BulkAssemblyConcatenationMethodType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BulkAssemblyConcatenationMethodType, getattr(newcls, "_UNKNOWN"))
