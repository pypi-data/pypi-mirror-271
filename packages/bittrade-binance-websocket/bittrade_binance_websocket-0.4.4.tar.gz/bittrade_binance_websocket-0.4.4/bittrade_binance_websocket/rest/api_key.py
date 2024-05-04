from typing import Any, Callable

from reactivex import Observable, just, throw
from reactivex import operators
import requests
from bittrade_binance_websocket.models import endpoints, request
from bittrade_binance_websocket.models.rest import CreateApiKeyRequest, DeleteApiKeyRequest, EditIpRestrictionsRequest, QueryApiKeyInformationRequest, QueryMarginApiKeyListRequest, QueryApiKeyInformationResponse, CreateApiKeyResponse, DeleteApiKeyResponse, EditIpRestrictionsResponse
from bittrade_binance_websocket.connection import http



def create_special_margin_api_key_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def create_special_margin_api_key_http(req: CreateApiKeyRequest) -> Observable[CreateApiKeyResponse]:
        def subscribe(observer, scheduler=None):
            endpoint = endpoints.BinanceEndpoints.MARGIN_SPECIAL_MARGIN_KEY
            msg = request.RequestMessage(
                method="POST",
                endpoint=endpoint,
                params=req.to_params(),
            )
            return http.send_request(
                add_token(
                    http.prepare_request(msg)
                )
            ).subscribe(observer, scheduler)
        return Observable(subscribe)
    
    return create_special_margin_api_key_http

def edit_special_margin_api_key_ip_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def edit_special_margin_api_key_ip_http(req: EditIpRestrictionsRequest) -> Observable[EditIpRestrictionsResponse]:
        def subscribe(observer, scheduler=None):
            endpoint = endpoints.BinanceEndpoints.MARGIN_SPECIAL_MARGIN_KEY_IP
            msg = request.RequestMessage(
                method="PUT",
                endpoint=endpoint,
                params=req.to_params(),
            )
            return http.send_request(
                add_token(
                    http.prepare_request(msg)
                )
            ).subscribe(observer, scheduler)
        return Observable(subscribe)
    
    return edit_special_margin_api_key_ip_http

def delete_special_margin_api_key_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def delete_special_margin_api_key_http(req: DeleteApiKeyRequest) -> Observable[DeleteApiKeyResponse]:
        def subscribe(observer, scheduler=None):
            endpoint = endpoints.BinanceEndpoints.MARGIN_SPECIAL_MARGIN_KEY
            msg = request.RequestMessage(
                method="DELETE",
                endpoint=endpoint,
                params=req.to_params(),
            )
            return http.send_request(
                add_token(
                    http.prepare_request(msg)
                )
            ).subscribe(observer, scheduler)
        return Observable(subscribe)
    
    return delete_special_margin_api_key_http


def query_special_margin_api_key_information_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def query_special_margin_api_key_information_http(req: QueryApiKeyInformationRequest) -> Observable[QueryApiKeyInformationResponse]:
        def subscribe(observer, scheduler=None):
            endpoint = endpoints.BinanceEndpoints.MARGIN_SPECIAL_MARGIN_KEY
            msg = request.RequestMessage(
                method="GET",
                endpoint=endpoint,
                params=req.to_params(),
            )
            return http.send_request(
                add_token(
                    http.prepare_request(msg)
                )
            ).subscribe(observer, scheduler)
        return Observable(subscribe)
    
    return query_special_margin_api_key_information_http

def query_special_margin_api_key_list_http_factory(
    add_token: Callable[[requests.models.Request], requests.models.Request]
):
    def query_special_margin_api_key_list_http(req: QueryMarginApiKeyListRequest) -> Observable[list[QueryApiKeyInformationResponse]]:
        def subscribe(observer, scheduler=None):
            endpoint = endpoints.BinanceEndpoints.MARGIN_SPECIAL_MARGIN_KEY_LIST
            msg = request.RequestMessage(
                method="GET",
                endpoint=endpoint,
                params=req.to_params(),
            )
            return http.send_request(
                add_token(
                    http.prepare_request(msg)
                )
            ).subscribe(observer, scheduler)
        return Observable(subscribe)
    
    return query_special_margin_api_key_list_http
