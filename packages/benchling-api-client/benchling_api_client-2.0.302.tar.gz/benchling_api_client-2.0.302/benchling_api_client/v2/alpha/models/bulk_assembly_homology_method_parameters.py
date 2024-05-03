from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.bulk_assembly_homology_method_parameters_ambiguous_construct_preference import (
    BulkAssemblyHomologyMethodParametersAmbiguousConstructPreference,
)
from ..models.bulk_assembly_homology_method_parameters_fragment_production_method import (
    BulkAssemblyHomologyMethodParametersFragmentProductionMethod,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkAssemblyHomologyMethodParameters")


@attr.s(auto_attribs=True, repr=False)
class BulkAssemblyHomologyMethodParameters:
    """  """

    _ambiguous_construct_preference: Union[
        Unset, BulkAssemblyHomologyMethodParametersAmbiguousConstructPreference
    ] = UNSET
    _fragment_production_method: Union[
        Unset, BulkAssemblyHomologyMethodParametersFragmentProductionMethod
    ] = UNSET

    def __repr__(self):
        fields = []
        fields.append("ambiguous_construct_preference={}".format(repr(self._ambiguous_construct_preference)))
        fields.append("fragment_production_method={}".format(repr(self._fragment_production_method)))
        return "BulkAssemblyHomologyMethodParameters({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        ambiguous_construct_preference: Union[Unset, int] = UNSET
        if not isinstance(self._ambiguous_construct_preference, Unset):
            ambiguous_construct_preference = self._ambiguous_construct_preference.value

        fragment_production_method: Union[Unset, int] = UNSET
        if not isinstance(self._fragment_production_method, Unset):
            fragment_production_method = self._fragment_production_method.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if ambiguous_construct_preference is not UNSET:
            field_dict["ambiguousConstructPreference"] = ambiguous_construct_preference
        if fragment_production_method is not UNSET:
            field_dict["fragmentProductionMethod"] = fragment_production_method

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_ambiguous_construct_preference() -> Union[
            Unset, BulkAssemblyHomologyMethodParametersAmbiguousConstructPreference
        ]:
            ambiguous_construct_preference = UNSET
            _ambiguous_construct_preference = d.pop("ambiguousConstructPreference")
            if _ambiguous_construct_preference is not None and _ambiguous_construct_preference is not UNSET:
                try:
                    ambiguous_construct_preference = (
                        BulkAssemblyHomologyMethodParametersAmbiguousConstructPreference(
                            _ambiguous_construct_preference
                        )
                    )
                except ValueError:
                    ambiguous_construct_preference = (
                        BulkAssemblyHomologyMethodParametersAmbiguousConstructPreference.of_unknown(
                            _ambiguous_construct_preference
                        )
                    )

            return ambiguous_construct_preference

        try:
            ambiguous_construct_preference = get_ambiguous_construct_preference()
        except KeyError:
            if strict:
                raise
            ambiguous_construct_preference = cast(
                Union[Unset, BulkAssemblyHomologyMethodParametersAmbiguousConstructPreference], UNSET
            )

        def get_fragment_production_method() -> Union[
            Unset, BulkAssemblyHomologyMethodParametersFragmentProductionMethod
        ]:
            fragment_production_method = UNSET
            _fragment_production_method = d.pop("fragmentProductionMethod")
            if _fragment_production_method is not None and _fragment_production_method is not UNSET:
                try:
                    fragment_production_method = BulkAssemblyHomologyMethodParametersFragmentProductionMethod(
                        _fragment_production_method
                    )
                except ValueError:
                    fragment_production_method = (
                        BulkAssemblyHomologyMethodParametersFragmentProductionMethod.of_unknown(
                            _fragment_production_method
                        )
                    )

            return fragment_production_method

        try:
            fragment_production_method = get_fragment_production_method()
        except KeyError:
            if strict:
                raise
            fragment_production_method = cast(
                Union[Unset, BulkAssemblyHomologyMethodParametersFragmentProductionMethod], UNSET
            )

        bulk_assembly_homology_method_parameters = cls(
            ambiguous_construct_preference=ambiguous_construct_preference,
            fragment_production_method=fragment_production_method,
        )

        return bulk_assembly_homology_method_parameters

    @property
    def ambiguous_construct_preference(
        self,
    ) -> BulkAssemblyHomologyMethodParametersAmbiguousConstructPreference:
        if isinstance(self._ambiguous_construct_preference, Unset):
            raise NotPresentError(self, "ambiguous_construct_preference")
        return self._ambiguous_construct_preference

    @ambiguous_construct_preference.setter
    def ambiguous_construct_preference(
        self, value: BulkAssemblyHomologyMethodParametersAmbiguousConstructPreference
    ) -> None:
        self._ambiguous_construct_preference = value

    @ambiguous_construct_preference.deleter
    def ambiguous_construct_preference(self) -> None:
        self._ambiguous_construct_preference = UNSET

    @property
    def fragment_production_method(self) -> BulkAssemblyHomologyMethodParametersFragmentProductionMethod:
        if isinstance(self._fragment_production_method, Unset):
            raise NotPresentError(self, "fragment_production_method")
        return self._fragment_production_method

    @fragment_production_method.setter
    def fragment_production_method(
        self, value: BulkAssemblyHomologyMethodParametersFragmentProductionMethod
    ) -> None:
        self._fragment_production_method = value

    @fragment_production_method.deleter
    def fragment_production_method(self) -> None:
        self._fragment_production_method = UNSET
