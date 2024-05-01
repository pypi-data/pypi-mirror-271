# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.remove_none_from_dict import remove_none_from_dict
from ..core.request_options import RequestOptions
from .types.automation_ad_hoc_invoke_params import AutomationAdHocInvokeParams
from .types.automation_invoke_params import AutomationInvokeParams
from .types.automation_invoke_response import AutomationInvokeResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class AutomationsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def invoke_automation_template(
        self,
        template_id: str,
        *,
        request: AutomationInvokeParams,
        idempotency_key: typing.Optional[str] = None,
        idempotency_expiry: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AutomationInvokeResponse:
        """
        Invoke an automation run from an automation template.

        Parameters
        ----------
        template_id : str
            A unique identifier representing the automation template to be invoked. This could be the Automation Template ID or the Automation Template Alias.

        request : AutomationInvokeParams

        idempotency_key : typing.Optional[str]

        idempotency_expiry : typing.Optional[str]
            The expiry can either be an ISO8601 datetime or a duration like "1 Day".

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AutomationInvokeResponse

        Examples
        --------
        from courier import AutomationInvokeParams
        from courier.client import Courier

        client = Courier(
            authorization_token="YOUR_AUTHORIZATION_TOKEN",
        )
        client.automations.invoke_automation_template(
            template_id="string",
            request=AutomationInvokeParams(
                brand="string",
                data={"string": {"key": "value"}},
                profile={"key": "value"},
                recipient="string",
                template="string",
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            method="POST",
            url=urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", f"automations/{jsonable_encoder(template_id)}/invoke"
            ),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        "Idempotency-Key": str(idempotency_key) if idempotency_key is not None else None,
                        "X-Idempotency-Expiration": str(idempotency_expiry) if idempotency_expiry is not None else None,
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(AutomationInvokeResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def invoke_ad_hoc_automation(
        self,
        *,
        request: AutomationAdHocInvokeParams,
        idempotency_key: typing.Optional[str] = None,
        idempotency_expiry: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AutomationInvokeResponse:
        """
        Invoke an ad hoc automation run. This endpoint accepts a JSON payload with a series of automation steps. For information about what steps are available, checkout the ad hoc automation guide [here](https://www.courier.com/docs/automations/steps/).

        Parameters
        ----------
        request : AutomationAdHocInvokeParams

        idempotency_key : typing.Optional[str]

        idempotency_expiry : typing.Optional[str]
            The expiry can either be an ISO8601 datetime or a duration like "1 Day".

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AutomationInvokeResponse

        Examples
        --------
        from courier import (
            Automation,
            AutomationAdHocInvokeParams,
            AutomationDelayStep,
            AutomationSendStep,
        )
        from courier.client import Courier

        client = Courier(
            authorization_token="YOUR_AUTHORIZATION_TOKEN",
        )
        client.automations.invoke_ad_hoc_automation(
            request=AutomationAdHocInvokeParams(
                data={"name": "Foo"},
                profile={"tenant_id": "abc-123"},
                recipient="user-yes",
                automation=Automation(
                    cancelation_token="delay-send--user-yes--abc-123",
                    steps=[
                        AutomationDelayStep(
                            action="delay",
                            until="20240408T080910.123",
                        ),
                        AutomationSendStep(
                            action="send",
                            template="64TP5HKPFTM8VTK1Y75SJDQX9JK0",
                        ),
                    ],
                ),
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "automations/invoke"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        "Idempotency-Key": str(idempotency_key) if idempotency_key is not None else None,
                        "X-Idempotency-Expiration": str(idempotency_expiry) if idempotency_expiry is not None else None,
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(AutomationInvokeResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncAutomationsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def invoke_automation_template(
        self,
        template_id: str,
        *,
        request: AutomationInvokeParams,
        idempotency_key: typing.Optional[str] = None,
        idempotency_expiry: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AutomationInvokeResponse:
        """
        Invoke an automation run from an automation template.

        Parameters
        ----------
        template_id : str
            A unique identifier representing the automation template to be invoked. This could be the Automation Template ID or the Automation Template Alias.

        request : AutomationInvokeParams

        idempotency_key : typing.Optional[str]

        idempotency_expiry : typing.Optional[str]
            The expiry can either be an ISO8601 datetime or a duration like "1 Day".

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AutomationInvokeResponse

        Examples
        --------
        from courier import AutomationInvokeParams
        from courier.client import AsyncCourier

        client = AsyncCourier(
            authorization_token="YOUR_AUTHORIZATION_TOKEN",
        )
        await client.automations.invoke_automation_template(
            template_id="string",
            request=AutomationInvokeParams(
                brand="string",
                data={"string": {"key": "value"}},
                profile={"key": "value"},
                recipient="string",
                template="string",
            ),
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            method="POST",
            url=urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", f"automations/{jsonable_encoder(template_id)}/invoke"
            ),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        "Idempotency-Key": str(idempotency_key) if idempotency_key is not None else None,
                        "X-Idempotency-Expiration": str(idempotency_expiry) if idempotency_expiry is not None else None,
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(AutomationInvokeResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def invoke_ad_hoc_automation(
        self,
        *,
        request: AutomationAdHocInvokeParams,
        idempotency_key: typing.Optional[str] = None,
        idempotency_expiry: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AutomationInvokeResponse:
        """
        Invoke an ad hoc automation run. This endpoint accepts a JSON payload with a series of automation steps. For information about what steps are available, checkout the ad hoc automation guide [here](https://www.courier.com/docs/automations/steps/).

        Parameters
        ----------
        request : AutomationAdHocInvokeParams

        idempotency_key : typing.Optional[str]

        idempotency_expiry : typing.Optional[str]
            The expiry can either be an ISO8601 datetime or a duration like "1 Day".

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AutomationInvokeResponse

        Examples
        --------
        from courier import (
            Automation,
            AutomationAdHocInvokeParams,
            AutomationDelayStep,
            AutomationSendStep,
        )
        from courier.client import AsyncCourier

        client = AsyncCourier(
            authorization_token="YOUR_AUTHORIZATION_TOKEN",
        )
        await client.automations.invoke_ad_hoc_automation(
            request=AutomationAdHocInvokeParams(
                data={"name": "Foo"},
                profile={"tenant_id": "abc-123"},
                recipient="user-yes",
                automation=Automation(
                    cancelation_token="delay-send--user-yes--abc-123",
                    steps=[
                        AutomationDelayStep(
                            action="delay",
                            until="20240408T080910.123",
                        ),
                        AutomationSendStep(
                            action="send",
                            template="64TP5HKPFTM8VTK1Y75SJDQX9JK0",
                        ),
                    ],
                ),
            ),
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "automations/invoke"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        "Idempotency-Key": str(idempotency_key) if idempotency_key is not None else None,
                        "X-Idempotency-Expiration": str(idempotency_expiry) if idempotency_expiry is not None else None,
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(AutomationInvokeResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
