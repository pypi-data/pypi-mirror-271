from typing import Literal
from bittrade_binance_websocket.models import endpoints, request
from bittrade_binance_websocket.models.rest.subaccount import UniversalTransferRequest, UserUniversalTransferRequest
from bittrade_binance_websocket.rest.http_factory_decorator import http_factory


@http_factory(None)  # type: ignore
def query_subaccount_list_http_factory():
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.SUBACCOUNT_LIST,
    )


@http_factory(None)  # type: ignore
def subaccount_universal_transfer_http_factory(r: UniversalTransferRequest):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.SUBACCOUNT_UNIVERSAL_TRANSFER,
        params=r.to_dict(),
    )

@http_factory(None)  # type: ignore
def user_universal_transfer_http_factory(r: UserUniversalTransferRequest):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.USER_UNIVERSAL_TRANSFER,
        params=r.to_dict(),
    )


@http_factory(None)  # type: ignore
def subaccount_transfer_to_master_http_factory(asset: str, amount: str):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.SUBACCOUNT_TO_MASTER_TRANSFER,
        params={
            "asset": asset,
            "amount": amount,
        },
    )

@http_factory(None)  # type: ignore
def subaccount_transfer_to_subaccount_http_factory(to_account: str, asset: str, amount: str):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.SUBACCOUNT_TO_SUBACCOUNT_TRANSFER,
        params={
            "toEmail": to_account,
            "asset": asset,
            "amount": amount,
        },
    )


@http_factory(None)  # type: ignore
def query_subaccount_margin_summary_http_factory():
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.SUBACCOUNT_SUMMARY,
    )

@http_factory(None)  # type: ignore
def query_subaccount_margin_detail_http_factory(email: str):
    return request.RequestMessage(
        method="GET",
        endpoint=endpoints.BinanceEndpoints.SUBACCOUNT_MARGIN_DETAIL,
        params={"email": email},
    )

@http_factory(None)  # type: ignore
def subaccount_add_ip_restriction_http_factory(email: str, api_key: str, status: Literal[1,2], ip_addresses: list[str]):
    return request.RequestMessage(
        method="POST",
        endpoint=endpoints.BinanceEndpoints.SUBACCOUNT_ADD_IP_RESTRICTION,
        params={
            "email": email,
            "subAccountApiKey": api_key,
            "status": status,
            "ipAddress": ",".join(ip_addresses),
        }
    )