# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1
from .elemental_base_node import ElementalBaseNode
from .i_alignment import IAlignment
from .locales import Locales
from .text_style import TextStyle


class ElementalQuoteNode(ElementalBaseNode):
    """
    Renders a quote block.
    """

    content: str = pydantic_v1.Field()
    """
    The text value of the quote.
    """

    align: typing.Optional[IAlignment] = pydantic_v1.Field(default=None)
    """
    Alignment of the quote.
    """

    border_color: typing.Optional[str] = pydantic_v1.Field(alias="borderColor", default=None)
    """
    CSS border color property. For example, `#fff`
    """

    text_style: TextStyle
    locales: Locales = pydantic_v1.Field()
    """
    Region specific content. See [locales docs](https://www.courier.com/docs/platform/content/elemental/locales/) for more details.
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
