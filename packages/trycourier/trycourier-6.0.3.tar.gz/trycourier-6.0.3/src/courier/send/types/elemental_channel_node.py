# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import pydantic_v1
from .elemental_base_node import ElementalBaseNode


class ElementalChannelNode(ElementalBaseNode):
    """
    The channel element allows a notification to be customized based on which channel it is sent through.
    For example, you may want to display a detailed message when the notification is sent through email,
    and a more concise message in a push notification. Channel elements are only valid as top-level
    elements; you cannot nest channel elements. If there is a channel element specified at the top-level
    of the document, all sibling elements must be channel elements.
    Note: As an alternative, most elements support a `channel` property. Which allows you to selectively
    display an individual element on a per channel basis. See the
    [control flow docs](https://www.courier.com/docs/platform/content/elemental/control-flow/) for more details.
    """

    channel: str = pydantic_v1.Field()
    """
    The channel the contents of this element should be applied to. Can be `email`,
    `push`, `direct_message`, `sms` or a provider such as slack
    """

    elements: typing.Optional[typing.List[ElementalNode]] = pydantic_v1.Field(default=None)
    """
    An array of elements to apply to the channel. If `raw` has not been
    specified, `elements` is `required`.
    """

    raw: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(default=None)
    """
    Raw data to apply to the channel. If `elements` has not been
    specified, `raw` is `required`.
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


from .elemental_node import ElementalNode  # noqa: E402

ElementalChannelNode.update_forward_refs()
