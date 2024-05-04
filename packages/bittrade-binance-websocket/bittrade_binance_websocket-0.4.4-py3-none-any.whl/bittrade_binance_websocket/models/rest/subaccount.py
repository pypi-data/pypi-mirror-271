from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class AccountType(Enum):
    SPOT = "SPOT"
    MARGIN = "MARGIN"
    ISOLATED_MARGIN = "ISOLATED_MARGIN"
    COIN_FUTURE = "COIN_FUTURE"
    USDT_FUTURE = "USDT_FUTURE"

@dataclass
class UniversalTransferRequest:
    from_email: str
    to_email: str
    from_account_type: AccountType
    to_account_type: AccountType
    asset: str
    amount: str
    transaction_id: str = ""
    symbol: str = ""

    def to_dict(self):
        data = {
            "fromEmail": self.from_email,
            "toEmail": self.to_email,
            "fromAccountType": self.from_account_type.value,
            "toAccountType": self.to_account_type.value,
            "asset": self.asset,
            "amount": self.amount,
            "transactionId": self.transaction_id,
            "symbol": self.symbol,
        }
        if self.symbol == "":
            del data["symbol"]
        if self.transaction_id == "":
            del data["transactionId"]
        if self.from_email == "":
            del data["fromEmail"]
        if self.to_email == "":
            del data["toEmail"]
        return data
    
class TransferType(Enum):
    MAIN_UMFUTURE = 'MAIN_UMFUTURE'  # Spot account transfer to USDⓈ-M Futures account
    MAIN_CMFUTURE = 'MAIN_CMFUTURE'  # Spot account transfer to COIN-M Futures account
    MAIN_MARGIN = 'MAIN_MARGIN'      # Spot account transfer to Margin（cross）account
    UMFUTURE_MAIN = 'UMFUTURE_MAIN'  # USDⓈ-M Futures account transfer to Spot account
    UMFUTURE_MARGIN = 'UMFUTURE_MARGIN' # USDⓈ-M Futures account transfer to Margin（cross）account
    CMFUTURE_MAIN = 'CMFUTURE_MAIN'  # COIN-M Futures account transfer to Spot account
    CMFUTURE_MARGIN = 'CMFUTURE_MARGIN' # COIN-M Futures account transfer to Margin(cross) account
    MARGIN_MAIN = 'MARGIN_MAIN'      # Margin（cross）account transfer to Spot account
    MARGIN_UMFUTURE = 'MARGIN_UMFUTURE' # Margin（cross）account transfer to USDⓈ-M Futures
    MARGIN_CMFUTURE = 'MARGIN_CMFUTURE' # Margin（cross）account transfer to COIN-M Futures
    ISOLATEDMARGIN_MARGIN = 'ISOLATEDMARGIN_MARGIN' # Isolated margin account transfer to Margin(cross) account
    MARGIN_ISOLATEDMARGIN = 'MARGIN_ISOLATEDMARGIN' # Margin(cross) account transfer to Isolated margin account
    ISOLATEDMARGIN_ISOLATEDMARGIN = 'ISOLATEDMARGIN_ISOLATEDMARGIN' # Isolated margin account transfer to Isolated margin account
    MAIN_FUNDING = 'MAIN_FUNDING'    # Spot account transfer to Funding account
    FUNDING_MAIN = 'FUNDING_MAIN'    # Funding account transfer to Spot account
    FUNDING_UMFUTURE = 'FUNDING_UMFUTURE' # Funding account transfer to UMFUTURE account
    UMFUTURE_FUNDING = 'UMFUTURE_FUNDING' # UMFUTURE account transfer to Funding account
    MARGIN_FUNDING = 'MARGIN_FUNDING' # MARGIN account transfer to Funding account
    FUNDING_MARGIN = 'FUNDING_MARGIN' # Funding account transfer to Margin account
    FUNDING_CMFUTURE = 'FUNDING_CMFUTURE' # Funding account transfer to CMFUTURE account
    CMFUTURE_FUNDING = 'CMFUTURE_FUNDING' # CMFUTURE account transfer to Funding account
    MAIN_OPTION = 'MAIN_OPTION'      # Spot account transfer to Options account
    OPTION_MAIN = 'OPTION_MAIN'      # Options account transfer to Spot account
    UMFUTURE_OPTION = 'UMFUTURE_OPTION' # USDⓈ-M Futures account transfer to Options account
    OPTION_UMFUTURE = 'OPTION_UMFUTURE' # Options account transfer to USDⓈ-M Futures account
    MARGIN_OPTION = 'MARGIN_OPTION'  # Margin（cross）account transfer to Options account
    OPTION_MARGIN = 'OPTION_MARGIN'  # Options account transfer to Margin（cross）account
    FUNDING_OPTION = 'FUNDING_OPTION' # Funding account transfer to Options account
    OPTION_FUNDING = 'OPTION_FUNDING' # Options account transfer to Funding account
    MAIN_PORTFOLIO_MARGIN = 'MAIN_PORTFOLIO_MARGIN' # Spot account transfer to Portfolio Margin account
    PORTFOLIO_MARGIN_MAIN = 'PORTFOLIO_MARGIN_MAIN' # Portfolio Margin account transfer to Spot account
    MAIN_ISOLATED_MARGIN = 'MAIN_ISOLATED_MARGIN' # Spot account transfer to Isolated margin account
    ISOLATED_MARGIN_MAIN = 'ISOLATED_MARGIN_MAIN' # Isolated margin account transfer to Spot account

@dataclass
class UserUniversalTransferRequest:
    type: TransferType
    asset: str
    amount: str
    from_symbol: str=""
    to_symbol: str=""

    def to_dict(self):
        data = {
            "type": self.type.value,
            "asset": self.asset,
            "amount": self.amount,
            "fromSymbol": self.from_symbol,
            "toSymbol": self.to_symbol,
        }
        if self.from_symbol == "":
            del data["fromSymbol"]
        if self.to_symbol == "":
            del data["toSymbol"]
        return data
