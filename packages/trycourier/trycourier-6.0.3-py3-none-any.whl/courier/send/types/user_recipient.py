# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1
from .i_profile_preferences import IProfilePreferences
from .message_context import MessageContext
from .message_data import MessageData
from .user_recipient_type import UserRecipientType


class UserRecipient(UserRecipientType):
    account_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Use `tenant_id` instad.
    """

    context: typing.Optional[MessageContext] = pydantic_v1.Field(default=None)
    """
    Context information such as tenant_id to send the notification with.
    """

    data: typing.Optional[MessageData] = None
    email: typing.Optional[str] = None
    locale: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    The user's preferred ISO 639-1 language code.
    """

    user_id: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    preferences: typing.Optional[IProfilePreferences] = None
    tenant_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    An id of a tenant, [see tenants api docs](https://www.courier.com/docs/reference/tenants).
    Will load brand, default preferences and any other base context data associated with this tenant.
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
        allow_population_by_field_name = True
        populate_by_name = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
