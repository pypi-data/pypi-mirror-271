# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1


class InboundBulkMessageV1(pydantic_v1.BaseModel):
    brand: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    A unique identifier that represents the brand that should be used
    for rendering the notification.
    """

    data: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(default=None)
    """
    JSON that includes any data you want to pass to a message template.
    The data will populate the corresponding template variables.
    """

    event: typing.Optional[str] = None
    locale: typing.Optional[typing.Dict[str, typing.Any]] = None
    override: typing.Optional[typing.Any] = pydantic_v1.Field(default=None)
    """
    JSON that is merged into the request sent by Courier to the provider
    to override properties or to gain access to features in the provider
    API that are not natively supported by Courier.
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
