from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.bulk_assembly_gibson_method_parameters import BulkAssemblyGibsonMethodParameters
from ..models.bulk_assembly_gibson_method_type import BulkAssemblyGibsonMethodType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkAssemblyGibsonMethod")


@attr.s(auto_attribs=True, repr=False)
class BulkAssemblyGibsonMethod:
    """  """

    _parameters: Union[Unset, BulkAssemblyGibsonMethodParameters] = UNSET
    _type: Union[Unset, BulkAssemblyGibsonMethodType] = UNSET

    def __repr__(self):
        fields = []
        fields.append("parameters={}".format(repr(self._parameters)))
        fields.append("type={}".format(repr(self._type)))
        return "BulkAssemblyGibsonMethod({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._parameters, Unset):
            parameters = self._parameters.to_dict()

        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_parameters() -> Union[Unset, BulkAssemblyGibsonMethodParameters]:
            parameters: Union[Unset, Union[Unset, BulkAssemblyGibsonMethodParameters]] = UNSET
            _parameters = d.pop("parameters")

            if not isinstance(_parameters, Unset):
                parameters = BulkAssemblyGibsonMethodParameters.from_dict(_parameters)

            return parameters

        try:
            parameters = get_parameters()
        except KeyError:
            if strict:
                raise
            parameters = cast(Union[Unset, BulkAssemblyGibsonMethodParameters], UNSET)

        def get_type() -> Union[Unset, BulkAssemblyGibsonMethodType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = BulkAssemblyGibsonMethodType(_type)
                except ValueError:
                    type = BulkAssemblyGibsonMethodType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, BulkAssemblyGibsonMethodType], UNSET)

        bulk_assembly_gibson_method = cls(
            parameters=parameters,
            type=type,
        )

        return bulk_assembly_gibson_method

    @property
    def parameters(self) -> BulkAssemblyGibsonMethodParameters:
        if isinstance(self._parameters, Unset):
            raise NotPresentError(self, "parameters")
        return self._parameters

    @parameters.setter
    def parameters(self, value: BulkAssemblyGibsonMethodParameters) -> None:
        self._parameters = value

    @parameters.deleter
    def parameters(self) -> None:
        self._parameters = UNSET

    @property
    def type(self) -> BulkAssemblyGibsonMethodType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: BulkAssemblyGibsonMethodType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
