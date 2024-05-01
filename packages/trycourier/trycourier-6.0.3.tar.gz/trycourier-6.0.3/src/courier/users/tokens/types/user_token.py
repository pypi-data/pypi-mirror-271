# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ....core.datetime_utils import serialize_datetime
from ....core.pydantic_utilities import pydantic_v1
from .device import Device
from .expiry_date import ExpiryDate
from .provider_key import ProviderKey
from .tracking import Tracking


class UserToken(pydantic_v1.BaseModel):
    token: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Full body of the token. Must match token in URL.
    """

    provider_key: ProviderKey
    expiry_date: typing.Optional[ExpiryDate] = pydantic_v1.Field(default=None)
    """
    ISO 8601 formatted date the token expires. Defaults to 2 months. Set to false to disable expiration.
    """

    properties: typing.Optional[typing.Any] = pydantic_v1.Field(default=None)
    """
    Properties sent to the provider along with the token
    """

    device: typing.Optional[Device] = pydantic_v1.Field(default=None)
    """
    Information about the device the token is associated with.
    """

    tracking: typing.Optional[Tracking] = pydantic_v1.Field(default=None)
    """
    Information about the device the token is associated with.
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
