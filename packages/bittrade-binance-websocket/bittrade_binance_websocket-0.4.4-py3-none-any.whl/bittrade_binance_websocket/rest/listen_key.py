from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import listen_key

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(listen_key.CreateListenKeyResponse)
def get_listen_key_http_factory():
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
    )


@http_factory(None)
def ping_listen_key_http_factory(listen_key: str):
    return request.RequestMessage(
        method="PUT",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
        params={
            "listenKey": listen_key,
        },
    )


@http_factory(listen_key.CreateListenKeyResponse)
def get_active_listen_key_http_factory():
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
    )


@http_factory(None)
def delete_listen_key_http_factory(listen_key: str):
    return request.RequestMessage(
        method="DELETE",
        endpoint=endpoints.BinanceEndpoints.LISTEN_KEY,
        params={
            "listenKey": listen_key,
        },
    )


@http_factory(listen_key.CreateListenKeyResponse)
def margin_get_listen_key_http_factory(symbol: str=""):
    """
    Get a listen key for the margin account.

    :param symbol: The isolated symbol to get the listen key for. If NOT provided, the listen key will be for the cross margin account.
    """
    is_isolated = bool(symbol)  # cross margin takes no symbol argument
    params = {"symbol": symbol} if is_isolated else {}
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.ISOLATED_MARGIN_LISTEN_KEY if is_isolated else endpoints.BinanceEndpoints.CROSS_MARGIN_LISTEN_KEY,
        params=params
    )


@http_factory(None)
def margin_ping_listen_key_http_factory(listen_key: str, symbol: str=""):
    """
    Ping the listen key for the margin account.

    :param listen_key: The listen key to ping.
    :param symbol: The isolated symbol to ping the listen key for. If NOT provided, the listen key will be for the cross margin account.
    """
    is_isolated = bool(symbol)  # cross margin takes no symbol argument
    params = {"listenKey": listen_key} | ({"symbol": symbol} if is_isolated else {})
    return request.RequestMessage(
        method="PUT",
        endpoint=endpoints.BinanceEndpoints.ISOLATED_MARGIN_LISTEN_KEY if is_isolated else endpoints.BinanceEndpoints.CROSS_MARGIN_LISTEN_KEY,
        params=params,
    )



@http_factory(None)
def margin_delete_listen_key_http_factory(listen_key: str, symbol: str=""):
    """
    Delete the listen key for the margin account.

    :param listen_key: The listen key to delete.
    :param symbol: The isolated symbol to delete the listen key for. If NOT provided, the listen key will be for the cross margin account.
    """
    is_isolated = bool(symbol)
    params = {"listenKey": listen_key} | ({"symbol": symbol} if is_isolated else {})
    return request.RequestMessage(
        method="DELETE",
        endpoint=endpoints.BinanceEndpoints.ISOLATED_MARGIN_LISTEN_KEY if is_isolated else endpoints.BinanceEndpoints.CROSS_MARGIN_LISTEN_KEY,
        params=params,
    )
