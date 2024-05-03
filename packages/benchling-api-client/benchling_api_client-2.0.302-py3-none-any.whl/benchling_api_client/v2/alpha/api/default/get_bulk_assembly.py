from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.bulk_assembly import BulkAssembly
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    bulk_assembly_id: str,
) -> Dict[str, Any]:
    url = "{}/bulk-assemblies/{bulk_assembly_id}".format(client.base_url, bulk_assembly_id=bulk_assembly_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[BulkAssembly]:
    if response.status_code == 200:
        response_200 = BulkAssembly.from_dict(response.json(), strict=False)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[BulkAssembly]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    bulk_assembly_id: str,
) -> Response[BulkAssembly]:
    kwargs = _get_kwargs(
        client=client,
        bulk_assembly_id=bulk_assembly_id,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    bulk_assembly_id: str,
) -> Optional[BulkAssembly]:
    """ Get a bulk assembly by its API identifier. """

    return sync_detailed(
        client=client,
        bulk_assembly_id=bulk_assembly_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    bulk_assembly_id: str,
) -> Response[BulkAssembly]:
    kwargs = _get_kwargs(
        client=client,
        bulk_assembly_id=bulk_assembly_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    bulk_assembly_id: str,
) -> Optional[BulkAssembly]:
    """ Get a bulk assembly by its API identifier. """

    return (
        await asyncio_detailed(
            client=client,
            bulk_assembly_id=bulk_assembly_id,
        )
    ).parsed
