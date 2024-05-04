from typing import Any, Callable

from reactivex import Observable, just, throw
from reactivex import operators
import requests
from bittrade_binance_websocket.models import endpoints
from bittrade_binance_websocket.models import request

from bittrade_binance_websocket.connection import http



def get_account_information_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def get_account_information_http(is_margin: bool=False, is_isolated: bool = False, symbols: list[str] | None = None):
        def subscribe(observer, scheduler=None):
            params = {}
            if is_isolated and symbols:
                params["symbols"] = ",".join(symbols)
            endpoint = endpoints.BinanceEndpoints.ACCOUNT_INFORMATION
            if is_margin:
                endpoint = endpoints.BinanceEndpoints.QUERY_CROSS_MARGIN_ACCOUNT_DETAILS
                if is_isolated:
                    endpoint = endpoints.BinanceEndpoints.QUERY_ISOLATED_MARGIN_ACCOUNT_DETAILS
            req = request.RequestMessage(
                method="GET",
                endpoint=endpoint,
                params=params,
            )
            return http.send_request(
                add_token(
                    http.prepare_request(req)
                )
            ).subscribe(observer, scheduler)
        return Observable(subscribe)
    
    return get_account_information_http
