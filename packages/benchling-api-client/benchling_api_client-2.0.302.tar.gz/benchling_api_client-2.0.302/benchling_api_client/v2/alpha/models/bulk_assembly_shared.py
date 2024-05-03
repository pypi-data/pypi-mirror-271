from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.bulk_assembly_shared_assembly_type import BulkAssemblySharedAssemblyType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkAssemblyShared")


@attr.s(auto_attribs=True, repr=False)
class BulkAssemblyShared:
    """  """

    _assembly_type: Union[Unset, BulkAssemblySharedAssemblyType] = UNSET
    _id: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("assembly_type={}".format(repr(self._assembly_type)))
        fields.append("id={}".format(repr(self._id)))
        return "BulkAssemblyShared({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        assembly_type: Union[Unset, int] = UNSET
        if not isinstance(self._assembly_type, Unset):
            assembly_type = self._assembly_type.value

        id = self._id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if assembly_type is not UNSET:
            field_dict["assemblyType"] = assembly_type
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_assembly_type() -> Union[Unset, BulkAssemblySharedAssemblyType]:
            assembly_type = UNSET
            _assembly_type = d.pop("assemblyType")
            if _assembly_type is not None and _assembly_type is not UNSET:
                try:
                    assembly_type = BulkAssemblySharedAssemblyType(_assembly_type)
                except ValueError:
                    assembly_type = BulkAssemblySharedAssemblyType.of_unknown(_assembly_type)

            return assembly_type

        try:
            assembly_type = get_assembly_type()
        except KeyError:
            if strict:
                raise
            assembly_type = cast(Union[Unset, BulkAssemblySharedAssemblyType], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        bulk_assembly_shared = cls(
            assembly_type=assembly_type,
            id=id,
        )

        return bulk_assembly_shared

    @property
    def assembly_type(self) -> BulkAssemblySharedAssemblyType:
        if isinstance(self._assembly_type, Unset):
            raise NotPresentError(self, "assembly_type")
        return self._assembly_type

    @assembly_type.setter
    def assembly_type(self, value: BulkAssemblySharedAssemblyType) -> None:
        self._assembly_type = value

    @assembly_type.deleter
    def assembly_type(self) -> None:
        self._assembly_type = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET
