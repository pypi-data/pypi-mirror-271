# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1
from .channel_identifier import ChannelIdentifier
from .routing_strategy_method import RoutingStrategyMethod


class RoutingStrategy(pydantic_v1.BaseModel):
    method: RoutingStrategyMethod = pydantic_v1.Field()
    """
    The method for selecting channels to send the message with. Value can be either 'single' or 'all'. If not provided will default to 'single'
    """

    channels: typing.List[ChannelIdentifier] = pydantic_v1.Field()
    """
    An array of valid channel identifiers (like email, push, sms, etc.) and additional routing nodes.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
