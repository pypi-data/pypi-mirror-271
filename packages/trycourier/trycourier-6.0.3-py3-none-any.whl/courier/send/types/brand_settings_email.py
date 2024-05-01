# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1
from .brand_template_override import BrandTemplateOverride
from .email_footer import EmailFooter
from .email_head import EmailHead
from .email_header import EmailHeader


class BrandSettingsEmail(pydantic_v1.BaseModel):
    template_override: typing.Optional[BrandTemplateOverride] = pydantic_v1.Field(
        alias="templateOverride", default=None
    )
    head: typing.Optional[EmailHead] = None
    footer: typing.Optional[EmailFooter] = None
    header: typing.Optional[EmailHeader] = None

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
