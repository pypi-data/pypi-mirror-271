# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1


class UserTenantAssociation(pydantic_v1.BaseModel):
    user_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    User ID for the assocation between tenant and user
    """

    type: typing.Optional[typing.Literal["user"]] = None
    tenant_id: str = pydantic_v1.Field()
    """
    Tenant ID for the assocation between tenant and user
    """

    profile: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(default=None)
    """
    Additional metadata to be applied to a user profile when used in a tenant context
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
