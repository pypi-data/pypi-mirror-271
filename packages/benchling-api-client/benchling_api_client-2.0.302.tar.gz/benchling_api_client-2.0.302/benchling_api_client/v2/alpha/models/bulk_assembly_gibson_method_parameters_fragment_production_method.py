from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BulkAssemblyGibsonMethodParametersFragmentProductionMethod(Enums.KnownString):
    EXISTING_HOMOLOGY_REGIONS = "EXISTING_HOMOLOGY_REGIONS"
    EXISTING_CUT_SITES = "EXISTING_CUT_SITES"
    PRIMER_PAIR = "PRIMER_PAIR"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BulkAssemblyGibsonMethodParametersFragmentProductionMethod":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BulkAssemblyGibsonMethodParametersFragmentProductionMethod must be a string (encountered: {val})"
            )
        newcls = Enum("BulkAssemblyGibsonMethodParametersFragmentProductionMethod", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BulkAssemblyGibsonMethodParametersFragmentProductionMethod, getattr(newcls, "_UNKNOWN"))
