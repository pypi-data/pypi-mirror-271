from typing import Any, Callable, Optional

from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models.rest import margin_account

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(dict)
def query_max_transfer_out_amount_http_factory(
    asset: str,
    isolated_symbol: Optional[str] = "",
):
    params = {"asset": asset}
    if isolated_symbol:
        params["isolatedSymbol"] = isolated_symbol
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.QUERY_MAX_TRANSFER_OUT_AMOUNT,
        params=params,
    )
