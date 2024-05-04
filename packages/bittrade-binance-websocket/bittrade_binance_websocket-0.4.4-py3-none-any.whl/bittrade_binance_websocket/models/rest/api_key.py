import dataclasses 
from typing import TypedDict

@dataclasses.dataclass
class CreateApiKeyRequest:
    name: str
    public_key: str = ""
    ips: list[str] = dataclasses.field(default_factory=list)
    symbol: str = ""

    def to_params(self):
        data = {
            "apiName": self.name,
            "ips": ",".join(self.ips),
        }
        if self.public_key:
            data["publicKey"] = self.public_key
        if self.symbol:
            data["symbol"] = self.symbol
        return data

CreateApiKeyResponse = TypedDict("CreateApiKeyResponse", {"apiKey": str, "type": str, "secretKey": str})

@dataclasses.dataclass
class DeleteApiKeyRequest:
    name: str = ""  # If apiName is given with no apiKey, all apikeys with given apiName will be deleted.
    api_key: str = ""  # If apiKey is given, apiName will be ignored.
    symbol: str = ""

    def to_params(self):
        data = {}
        if self.name:
            data["apiName"] = self.name
        if self.api_key:
            data["apiKey"] = self.api_key
        if self.symbol:
            data["symbol"] = self.symbol
        return data
    
DeleteApiKeyResponse = TypedDict("DeleteApiKeyResponse", {})

@dataclasses.dataclass
class EditIpRestrictionsRequest:
    api_key: str
    ip: list[str] = dataclasses.field(default_factory=list)
    symbol: str = ""

    def to_params(self):
        data = {
            "apiKey": self.api_key,
            "ip": ",".join(self.ip),
        }
        if self.symbol:
            data["symbol"] = self.symbol
        return data
    
EditIpRestrictionsResponse = TypedDict("EditIpRestrictionsResponse", {})


@dataclasses.dataclass
class QueryApiKeyInformationRequest:
    api_key: str
    symbol: str = ""

    def to_params(self):
        data = {
            "apiKey": self.api_key,
        }
        if self.symbol:
            data["symbol"] = self.symbol
        return data
    
QueryApiKeyInformationResponse = TypedDict("QueryApiKeyInformationResponse", {"apiKey": str, "type": str, "ip": str, "apiName": str})

@dataclasses.dataclass
class QueryMarginApiKeyListRequest:
    symbol: str = ""

    def to_params(self):
        data = {}
        if self.symbol:
            data["symbol"] = self.symbol
        return data
    
