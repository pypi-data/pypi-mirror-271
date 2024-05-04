from typing import Any, Callable, Optional, cast

from reactivex import Observable
import requests

from bittrade_binance_websocket.connection import http
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request
from bittrade_binance_websocket.models import order

from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


def cancel_order_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def cancel_order_http(params: order.OrderCancelRequest):
        def subscribe(observer, scheduler=None):
            req = request.RequestMessage(
                method="DELETE",
                endpoint=endpoints.BinanceEndpoints.MARGIN_ORDER
                if params.is_margin
                else endpoints.BinanceEndpoints.SPOT_ORDER,
                params=params.to_dict(),
            )
            return http.send_request(
                add_token(
                    http.prepare_request(req)
                )
            ).subscribe(observer, scheduler)
        return cast(Observable[order.SymbolOrderResponseItem], Observable(subscribe))
    return cancel_order_http