from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BulkAssemblyGoldenGateMethodParametersFragmentProductionMethod(Enums.KnownString):
    PRIMER_PAIR = "PRIMER_PAIR"
    EXISTING_CUT_SITES = "EXISTING_CUT_SITES"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BulkAssemblyGoldenGateMethodParametersFragmentProductionMethod":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BulkAssemblyGoldenGateMethodParametersFragmentProductionMethod must be a string (encountered: {val})"
            )
        newcls = Enum("BulkAssemblyGoldenGateMethodParametersFragmentProductionMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(
            BulkAssemblyGoldenGateMethodParametersFragmentProductionMethod, getattr(newcls, "_UNKNOWN")
        )
