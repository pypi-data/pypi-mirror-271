import json
from typing import *

import httpx

from ..api_config import APIConfig, HTTPException
from ..models import *


async def HardwaresResource_get_get(
    type: Optional[Union[str, None]] = None,
    api_config_override: Optional[APIConfig] = None,
) -> Paginated_HardwareObjectSchema_:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/api/hardware"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }
    query_params: Dict[str, Any] = {"type": type}

    query_params = {
        key: value for (key, value) in query_params.items() if value is not None
    }

    async with httpx.AsyncClient(
        base_url=base_path, verify=api_config.verify
    ) as client:
        response = await client.request(
            "get",
            httpx.URL(path),
            headers=headers,
            params=query_params,
        )

    if response.status_code != 200:
        from blissclient import parse_http_error_response

        parse_http_error_response(response)
        raise HTTPException(
            response.status_code, f" failed with status code: {response.status_code}"
        )

    return (
        Paginated_HardwareObjectSchema_(**response.json())
        if response.json() is not None
        else Paginated_HardwareObjectSchema_()
    )


async def RegisterHardwareResource_post_register_post(
    data: RegisterHardwareSchema, api_config_override: Optional[APIConfig] = None
) -> RegisterHardwareSchema:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/api/hardware/register"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }
    query_params: Dict[str, Any] = {}

    query_params = {
        key: value for (key, value) in query_params.items() if value is not None
    }

    async with httpx.AsyncClient(
        base_url=base_path, verify=api_config.verify
    ) as client:
        response = await client.request(
            "post",
            httpx.URL(path),
            headers=headers,
            params=query_params,
            json=data.dict(),
        )

    if response.status_code != 200:
        from blissclient import parse_http_error_response

        parse_http_error_response(response)
        raise HTTPException(
            response.status_code, f" failed with status code: {response.status_code}"
        )

    return (
        RegisterHardwareSchema(**response.json())
        if response.json() is not None
        else RegisterHardwareSchema()
    )


async def HardwareResource_get__string_id__get(
    id: str, api_config_override: Optional[APIConfig] = None
) -> HardwareObjectSchema:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/api/hardware/{id}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }
    query_params: Dict[str, Any] = {}

    query_params = {
        key: value for (key, value) in query_params.items() if value is not None
    }

    async with httpx.AsyncClient(
        base_url=base_path, verify=api_config.verify
    ) as client:
        response = await client.request(
            "get",
            httpx.URL(path),
            headers=headers,
            params=query_params,
        )

    if response.status_code != 200:
        from blissclient import parse_http_error_response

        parse_http_error_response(response)
        raise HTTPException(
            response.status_code, f" failed with status code: {response.status_code}"
        )

    return (
        HardwareObjectSchema(**response.json())
        if response.json() is not None
        else HardwareObjectSchema()
    )


async def HardwareResource_post__string_id__post(
    id: str, data: CallObjectFunction, api_config_override: Optional[APIConfig] = None
) -> CallObjectFunctionResponse:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/api/hardware/{id}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }
    query_params: Dict[str, Any] = {}

    query_params = {
        key: value for (key, value) in query_params.items() if value is not None
    }

    async with httpx.AsyncClient(
        base_url=base_path, verify=api_config.verify
    ) as client:
        response = await client.request(
            "post",
            httpx.URL(path),
            headers=headers,
            params=query_params,
            json=data.dict(),
        )

    if response.status_code != 200:
        from blissclient import parse_http_error_response

        parse_http_error_response(response)
        raise HTTPException(
            response.status_code, f" failed with status code: {response.status_code}"
        )

    return (
        CallObjectFunctionResponse(**response.json())
        if response.json() is not None
        else CallObjectFunctionResponse()
    )


async def HardwareResource_put__string_id__put(
    id: str, data: SetObjectProperty, api_config_override: Optional[APIConfig] = None
) -> SetObjectProperty:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/api/hardware/{id}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }
    query_params: Dict[str, Any] = {}

    query_params = {
        key: value for (key, value) in query_params.items() if value is not None
    }

    async with httpx.AsyncClient(
        base_url=base_path, verify=api_config.verify
    ) as client:
        response = await client.request(
            "put",
            httpx.URL(path),
            headers=headers,
            params=query_params,
            json=data.dict(),
        )

    if response.status_code != 200:
        from blissclient import parse_http_error_response

        parse_http_error_response(response)
        raise HTTPException(
            response.status_code, f" failed with status code: {response.status_code}"
        )

    return (
        SetObjectProperty(**response.json())
        if response.json() is not None
        else SetObjectProperty()
    )
