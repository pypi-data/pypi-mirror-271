from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.bulk_assembly_constant_bin import BulkAssemblyConstantBin
from ..models.bulk_assembly_fragment_bin import BulkAssemblyFragmentBin
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkAssembly")


@attr.s(auto_attribs=True, repr=False)
class BulkAssembly:
    """ Bulk assembly object. """

    _bins: Union[Unset, List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("bins={}".format(repr(self._bins)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "BulkAssembly({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        bins: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._bins, Unset):
            bins = []
            for bins_item_data in self._bins:
                if isinstance(bins_item_data, UnknownType):
                    bins_item = bins_item_data.value
                elif isinstance(bins_item_data, BulkAssemblyFragmentBin):
                    bins_item = bins_item_data.to_dict()

                else:
                    bins_item = bins_item_data.to_dict()

                bins.append(bins_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if bins is not UNSET:
            field_dict["bins"] = bins

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_bins() -> Union[
            Unset, List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]
        ]:
            bins = []
            _bins = d.pop("bins")
            for bins_item_data in _bins or []:

                def _parse_bins_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]:
                    bins_item: Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]
                    discriminator_value: str = cast(str, data.get("binType"))
                    if discriminator_value is not None:

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        bins_item = BulkAssemblyFragmentBin.from_dict(data, strict=True)

                        return bins_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        bins_item = BulkAssemblyConstantBin.from_dict(data, strict=True)

                        return bins_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                bins_item = _parse_bins_item(bins_item_data)

                bins.append(bins_item)

            return bins

        try:
            bins = get_bins()
        except KeyError:
            if strict:
                raise
            bins = cast(
                Union[Unset, List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]],
                UNSET,
            )

        bulk_assembly = cls(
            bins=bins,
        )

        bulk_assembly.additional_properties = d
        return bulk_assembly

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def bins(self) -> List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]:
        if isinstance(self._bins, Unset):
            raise NotPresentError(self, "bins")
        return self._bins

    @bins.setter
    def bins(self, value: List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]) -> None:
        self._bins = value

    @bins.deleter
    def bins(self) -> None:
        self._bins = UNSET
