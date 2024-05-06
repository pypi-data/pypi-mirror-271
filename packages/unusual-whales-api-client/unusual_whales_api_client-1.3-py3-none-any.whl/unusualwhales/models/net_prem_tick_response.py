from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NetPremTickResponse")


@_attrs_define
class NetPremTickResponse:
    """The net premium for each trading minute.

    Example:
        {'data': [{'date': datetime.date(2023, 9, 7), 'net_call_premium': '-2075581.0000', 'net_call_volume': -2259,
            'net_put_premium': '-15559.0000', 'net_put_volume': 95, 'tape_time': datetime.datetime(2023, 9, 7, 9, 30,
            tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)))}, {'date': datetime.date(2023, 9, 7),
            'net_call_premium': '670064.0000', 'net_call_volume': 754, 'net_put_premium': '-1480020.0000', 'net_put_volume':
            -264, 'tape_time': datetime.datetime(2023, 9, 7, 9, 31, tzinfo=datetime.timezone(datetime.timedelta(days=-1,
            seconds=72000)))}, {'date': datetime.date(2023, 9, 7), 'net_call_premium': '128926.0000', 'net_call_volume':
            1347, 'net_put_premium': '-644069.0000', 'net_put_volume': 2181, 'tape_time': datetime.datetime(2023, 9, 7, 9,
            32, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)))}, {'date': datetime.date(2023, 9, 7),
            'net_call_premium': '-1095135.0000', 'net_call_volume': 1049, 'net_put_premium': '135732.0000',
            'net_put_volume': 415, 'tape_time': datetime.datetime(2023, 9, 7, 9, 33,
            tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)))}, {'date': datetime.date(2023, 9, 7),
            'net_call_premium': '165842.0000', 'net_call_volume': 429, 'net_put_premium': '-379365.0000', 'net_put_volume':
            224, 'tape_time': datetime.datetime(2023, 9, 7, 9, 34, tzinfo=datetime.timezone(datetime.timedelta(days=-1,
            seconds=72000)))}, {'date': datetime.date(2023, 9, 7), 'net_call_premium': '376569.0000', 'net_call_volume':
            1002, 'net_put_premium': '408447.0000', 'net_put_volume': 1313, 'tape_time': datetime.datetime(2023, 9, 7, 9,
            35, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)))}, {'date': datetime.date(2023, 9, 7),
            'net_call_premium': '1528190.0000', 'net_call_volume': 4616, 'net_put_premium': '-1385094.0000',
            'net_put_volume': -3197, 'tape_time': datetime.datetime(2023, 9, 7, 9, 36,
            tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)))}, {'date': datetime.date(2023, 9, 7),
            'net_call_premium': '646507.0000', 'net_call_volume': 565, 'net_put_premium': '-171857.0000', 'net_put_volume':
            -351, 'tape_time': datetime.datetime(2023, 9, 7, 9, 37, tzinfo=datetime.timezone(datetime.timedelta(days=-1,
            seconds=72000)))}]}

    Attributes:
        net_call_premium (Union[Unset, str]): Defined as (call premium ask side) - (call premium bid side). Example:
            -29138464.
        net_call_volume (Union[Unset, int]): Defined as (call volume ask side) - (call volume bid side). Example: 1049.
        net_put_premium (Union[Unset, str]): Defined as (put premium ask side) - (put premium bid side). Example:
            23924325.
        net_put_volume (Union[Unset, int]): Defined as (put volume ask side) - (put volume bid side). Example: 1313.
        tape_time (Union[Unset, str]): The start time of the tick as a timestamp with timezone. Example: 2023-09-07
            09:30:00-04:00.
    """

    net_call_premium: Union[Unset, str] = UNSET
    net_call_volume: Union[Unset, int] = UNSET
    net_put_premium: Union[Unset, str] = UNSET
    net_put_volume: Union[Unset, int] = UNSET
    tape_time: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        net_call_premium = self.net_call_premium

        net_call_volume = self.net_call_volume

        net_put_premium = self.net_put_premium

        net_put_volume = self.net_put_volume

        tape_time = self.tape_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if net_call_premium is not UNSET:
            field_dict["net_call_premium"] = net_call_premium
        if net_call_volume is not UNSET:
            field_dict["net_call_volume"] = net_call_volume
        if net_put_premium is not UNSET:
            field_dict["net_put_premium"] = net_put_premium
        if net_put_volume is not UNSET:
            field_dict["net_put_volume"] = net_put_volume
        if tape_time is not UNSET:
            field_dict["tape_time"] = tape_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        net_call_premium = d.pop("net_call_premium", UNSET)

        net_call_volume = d.pop("net_call_volume", UNSET)

        net_put_premium = d.pop("net_put_premium", UNSET)

        net_put_volume = d.pop("net_put_volume", UNSET)

        tape_time = d.pop("tape_time", UNSET)

        net_prem_tick_response = cls(
            net_call_premium=net_call_premium,
            net_call_volume=net_call_volume,
            net_put_premium=net_put_premium,
            net_put_volume=net_put_volume,
            tape_time=tape_time,
        )

        net_prem_tick_response.additional_properties = d
        return net_prem_tick_response

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
