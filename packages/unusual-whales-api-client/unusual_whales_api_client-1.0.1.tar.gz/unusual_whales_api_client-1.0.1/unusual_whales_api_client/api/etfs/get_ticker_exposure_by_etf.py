from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.holdings import Holdings
from ...types import Response


def _get_kwargs(
    ticker: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/etfs/{ticker}/exposure",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Holdings]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Holdings.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Holdings]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    ticker: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Holdings]:
    """Ticker Exposure by ETF

     Returns all ETFs in which the given ticker is a holding

    Args:
        ticker (str): A single ticker Example: AAPL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Holdings]
    """

    kwargs = _get_kwargs(
        ticker=ticker,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    ticker: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Holdings]:
    """Ticker Exposure by ETF

     Returns all ETFs in which the given ticker is a holding

    Args:
        ticker (str): A single ticker Example: AAPL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Holdings
    """

    return sync_detailed(
        ticker=ticker,
        client=client,
    ).parsed


async def asyncio_detailed(
    ticker: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Holdings]:
    """Ticker Exposure by ETF

     Returns all ETFs in which the given ticker is a holding

    Args:
        ticker (str): A single ticker Example: AAPL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Holdings]
    """

    kwargs = _get_kwargs(
        ticker=ticker,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    ticker: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Holdings]:
    """Ticker Exposure by ETF

     Returns all ETFs in which the given ticker is a holding

    Args:
        ticker (str): A single ticker Example: AAPL.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Holdings
    """

    return (
        await asyncio_detailed(
            ticker=ticker,
            client=client,
        )
    ).parsed
