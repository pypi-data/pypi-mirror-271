from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/socket",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    r"""Unusual Whales websocket channels

     Returns the available WebSocket channels for connections.

    ## Websocket Guide
    Important: Websockets are not part of the basic API subscription. To be able to connect to
    WebSockets, please
    contact us at support@unusualwhales.com.

    The following channels are available:
    | Channel              | Description
    |
    |----------------------|----------------------------------------------------------------------------
    -------------------------------------------|
    | option_trades        | Receive all option trades live through out the trading session
    |
    | option_trades:TICKER | Similar to `option_trades` but receive all trades only for the specified
    ticker                                       |
    | flow-alerts          | Receive all flow alerts. The data can be used to build a similar view as
    https://unusualwhales.com/option-flow-alerts |
    | price:TICKER         | Receive live price updates for the given ticker.
    |

    The `option_trades` channel will stream all 6,000,000 option trades in real-time,
    `option_trades:<TICKER>` will stream
    all option trades for the given ticker in real-time.

    `flow-alerts` will stream from the alerts [page](https://unusualwhales.com/option-flow-
    alerts?limit=50)

    ## Connect
    We will use [websocat](https://github.com/vi/websocat) to demonstrate how to connect to the
    WebSocket server.

    ```bash
    websocat \"wss://api.unusualwhales.com/socket?token=<YOUR_API_TOKEN>\"
    {\"channel\":\"option_trades\",\"msg_type\":\"join\"}
    ```
    The server will then reply with
    ```bash
    [\"option_trades\",{\"response\":{},\"status\":\"ok\"}]
    ```
    indicating that the connection was successful.

    You will then receive data in the following format:
    ```bash
    [<CHANNEL_NAME>, <PAYLOAD>]
    ```
    during market hours.

    To receive the trades only for a specific ticker, use the following command:
    ```bash
    {\"channel\":\"option_trades\",\"msg_type\":\"join\"}
    ```

    You can join multiple channels with the same websocket connection:
    ```bash
    websocat \"wss://api.unusualwhales.com/socket?token=<YOUR_API_TOKEN>\"
    {\"channel\":\"option_trades\",\"msg_type\":\"join\"}
    [\"option_trades\",{\"response\":{},\"status\":\"ok\"}]
    {\"channel\":\"option_trades:JPM\",\"msg_type\":\"join\"}
    [\"option_trades:JPM\",{\"response\":{},\"status\":\"ok\"}]
    ```

    ## Using a client
    If you are using Python, you can use the [websocket-client](https://github.com/websocket-
    client/websocket-client) library to connect to the server.

    ```python
    import websocket
    import time
    import rel
    import json

    def on_message(ws, msg):
        msg = json.loads(msg)
        channel, payload = msg
        print(f\"Got a message on channel {channel}: Payload: {payload}\")

    def on_error(ws, error):
        print(error)

    def on_close(ws, close_status_code, close_msg):
        print(\"### closed ###\")

    def on_open(ws):
        print(\"Opened connection\")
        msg = {\"channel\":\"option_trades\",\"msg_type\":\"join\"}
        ws.send(json.dumps(msg))

    if __name__ == \"__main__\":
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(\"wss://api.unusualwhales.com/socket?token=<YOUR_TOKEN>\",
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)

        ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5
    second reconnect delay if connection closed unexpectedly
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()


    ## Historic data
    To download/access historic data, use the endpoint [/api/option-trades/full-
    tape](https://api.unusualwhales.com/docs#/operations/PublicApi.OptionTradeController.full_tape)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    r"""Unusual Whales websocket channels

     Returns the available WebSocket channels for connections.

    ## Websocket Guide
    Important: Websockets are not part of the basic API subscription. To be able to connect to
    WebSockets, please
    contact us at support@unusualwhales.com.

    The following channels are available:
    | Channel              | Description
    |
    |----------------------|----------------------------------------------------------------------------
    -------------------------------------------|
    | option_trades        | Receive all option trades live through out the trading session
    |
    | option_trades:TICKER | Similar to `option_trades` but receive all trades only for the specified
    ticker                                       |
    | flow-alerts          | Receive all flow alerts. The data can be used to build a similar view as
    https://unusualwhales.com/option-flow-alerts |
    | price:TICKER         | Receive live price updates for the given ticker.
    |

    The `option_trades` channel will stream all 6,000,000 option trades in real-time,
    `option_trades:<TICKER>` will stream
    all option trades for the given ticker in real-time.

    `flow-alerts` will stream from the alerts [page](https://unusualwhales.com/option-flow-
    alerts?limit=50)

    ## Connect
    We will use [websocat](https://github.com/vi/websocat) to demonstrate how to connect to the
    WebSocket server.

    ```bash
    websocat \"wss://api.unusualwhales.com/socket?token=<YOUR_API_TOKEN>\"
    {\"channel\":\"option_trades\",\"msg_type\":\"join\"}
    ```
    The server will then reply with
    ```bash
    [\"option_trades\",{\"response\":{},\"status\":\"ok\"}]
    ```
    indicating that the connection was successful.

    You will then receive data in the following format:
    ```bash
    [<CHANNEL_NAME>, <PAYLOAD>]
    ```
    during market hours.

    To receive the trades only for a specific ticker, use the following command:
    ```bash
    {\"channel\":\"option_trades\",\"msg_type\":\"join\"}
    ```

    You can join multiple channels with the same websocket connection:
    ```bash
    websocat \"wss://api.unusualwhales.com/socket?token=<YOUR_API_TOKEN>\"
    {\"channel\":\"option_trades\",\"msg_type\":\"join\"}
    [\"option_trades\",{\"response\":{},\"status\":\"ok\"}]
    {\"channel\":\"option_trades:JPM\",\"msg_type\":\"join\"}
    [\"option_trades:JPM\",{\"response\":{},\"status\":\"ok\"}]
    ```

    ## Using a client
    If you are using Python, you can use the [websocket-client](https://github.com/websocket-
    client/websocket-client) library to connect to the server.

    ```python
    import websocket
    import time
    import rel
    import json

    def on_message(ws, msg):
        msg = json.loads(msg)
        channel, payload = msg
        print(f\"Got a message on channel {channel}: Payload: {payload}\")

    def on_error(ws, error):
        print(error)

    def on_close(ws, close_status_code, close_msg):
        print(\"### closed ###\")

    def on_open(ws):
        print(\"Opened connection\")
        msg = {\"channel\":\"option_trades\",\"msg_type\":\"join\"}
        ws.send(json.dumps(msg))

    if __name__ == \"__main__\":
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(\"wss://api.unusualwhales.com/socket?token=<YOUR_TOKEN>\",
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)

        ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5
    second reconnect delay if connection closed unexpectedly
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()


    ## Historic data
    To download/access historic data, use the endpoint [/api/option-trades/full-
    tape](https://api.unusualwhales.com/docs#/operations/PublicApi.OptionTradeController.full_tape)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
