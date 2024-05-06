from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OptionChainsResponse")


@_attrs_define
class OptionChainsResponse:
    """All option chains for a given ticker.

    Example:
        {'data': ['AAPL230908C00175000', 'AAPL231020C00185000', 'AAPL230908C00180000', 'AAPL230908C00182500',
            'AAPL230908C00185000', 'AAPL230908C00187500', 'AAPL230908P00172500', 'AAPL230908P00175000',
            'AAPL230908P00177500', 'AAPL230908C00177500', 'AAPL230915C00177500', 'AAPL230915C00180000',
            'AAPL230915C00185000', 'AAPL230915C00187500', 'AAPL230915C00192500', 'AAPL230915C00195000',
            'AAPL230915C00200000']}

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        option_chains_response = cls()

        option_chains_response.additional_properties = d
        return option_chains_response

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
