from .request import RequestBody
from .base import (
    Assets,
    PaidButtons,
    InvoiceStatus,
    CurrencyType,
    CheckStatus,
)
from loguru import logger
from .profile import Profile
from .balance import Balance
from .rates import ExchangeRate
from .currencies import Currency
from .invoice import Invoice
from .transfer import Transfer
from .check import Check
from .app_stats import AppStats
from .exchange import getRate, getRateSumm

from datetime import datetime
from typing import Optional, Union, List, Callable
class TeleCryptoBot:

    def __init__(self,key) -> None:
        self.apikey = key

    def getMe(self) -> Profile:
        response = RequestBody.req(self, key=self.apikey, method="getMe")
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
                return Profile(**response["result"])

    def createInvoice(
        self,
        amount: Union[int, float],
        asset: Optional[Union[Assets, str]] = None,
        description: Optional[str] = None,
        hidden_message: Optional[str] = None,
        paid_btn_name: Optional[Union[PaidButtons, str]] = None,
        paid_btn_url: Optional[str] = None,
        payload: Optional[str] = None,
        allow_comments: Optional[bool] = None,
        allow_anonymous: Optional[bool] = None,
        expires_in: Optional[int] = None,
        fiat: Optional[str] = None,
        currency_type: Optional[Union[CurrencyType, str]] = None,
        accepted_assets: Optional[Union[List[Union[Assets, str]], str]] = None,
    ) -> Invoice:
            if accepted_assets and type(accepted_assets) == list:
                accepted_assets = ",".join(map(str, accepted_assets))

            params = {
                "asset": asset,
                "amount": amount,
                "description": description,
                "hidden_message": hidden_message,
                "paid_btn_name": paid_btn_name,
                "paid_btn_url": paid_btn_url,
                "payload": payload,
                "allow_comments": allow_comments,
                "allow_anonymous": allow_anonymous,
                "expires_in": expires_in,
                "fiat": fiat,
                "currency_type": currency_type,
                "accepted_assets": accepted_assets,
            }
            response = RequestBody.req(self, key=self.apikey, method="createInvoice", data=params)
            if isinstance(response, str):
                logger.error(response)
                return False
            else:
                return Invoice(**response["result"])

    def deleteInvoice(self,invoice_id: int) -> bool:
        params = {
            "invoice_id": invoice_id
        }
        response = RequestBody.req(self, key=self.apikey, method="deleteInvoice", data=params)
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
                return response['result']

    def createCheck(
        self,
        asset: Union[Assets, str],
        amount: Union[int, float],
        pin_to_user_id: Optional[int] = None,
        pin_to_username: Optional[str] = None,
    ) -> Check:
        params = {
            "asset": asset,
            "amount": amount,
            "pin_to_username": pin_to_username,
            "pin_to_user_id": pin_to_user_id
        }
        response = RequestBody.req(self, key=self.apikey, method="createCheck", data=params)
        return Check(**response["result"])

    def deleteCheck(self, check_id: int) -> bool:
        params = {
            "check_id": check_id
        }
        response = RequestBody.req(self, key=self.apikey, method="deleteCheck", data=params)
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
                return response["result"]

    def transfer(
        self,
        user_id: int,
        asset: Union[Assets, str],
        amount: Union[int, float],
        spend_id: Union[str, int],
        comment: Optional[str] = None,
        disable_send_notification: Optional[bool] = None,
    ) -> Transfer:        
        params = {
            "user_id": user_id,
            "asset": asset,
            "amount": amount,
            "spend_id": spend_id,
            "comment": comment,
            "disable_send_notification": disable_send_notification,
            }
        response = RequestBody.req(self, key=self.apikey, method="transfer", data=params)
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
                return Transfer(**response["result"])

    def getInvoices(
        self,
        asset: Optional[Union[Assets, str]] = None,
        invoice_ids: Optional[Union[List[int], int]] = None,
        status: Optional[Union[InvoiceStatus, str]] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Optional[Union[Invoice, List[Invoice]]]:
        if invoice_ids and type(invoice_ids) == list:
            invoice_ids = ",".join(map(str, invoice_ids))
        params = {
            "asset": asset,
            "invoice_ids": invoice_ids,
            "status": status,
            "offset": offset,
            "count": count,
            }
        response = RequestBody.req(self, key=self.apikey, method="getInvoices", data=params)
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
                if len(response["result"]["items"]) > 0:
                    if invoice_ids and isinstance(invoice_ids, int):
                        return Invoice(**response["result"]["items"][0])
                return [Invoice(**invoice) for invoice in response["result"]["items"]]

    def getTransfers(
        self,
        asset: Optional[Union[Assets, str]] = None,
        transfer_ids: Optional[Union[List[int], int]] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Optional[Union[Transfer, List[Transfer]]]:
        if transfer_ids and type(transfer_ids) == list:
            transfer_ids = ",".join(map(str, transfer_ids))
        params = {
            "asset": asset,
            "transfer_ids": transfer_ids,
            "offset": offset,
            "count": count,
            }
        response = RequestBody.req(self, key=self.apikey, method="getTransfers", data=params)
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
                if len(response["result"]["items"]) > 0:
                    if transfer_ids and isinstance(transfer_ids, int):
                        return Transfer(**response["result"]["items"][0])
                return [Transfer(**transfer) for transfer in response["result"]["items"]]

    def getChecks(
        self,
        asset: Optional[Union[Assets, str]] = None,
        check_ids: Optional[Union[List[int], int]] = None,
        status: Optional[Union[CheckStatus, str]] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> Check:
        if check_ids and type(check_ids) == list:
            check_ids = ",".join(map(str, check_ids))
        params = {
            "asset": asset,
            "check_ids": check_ids,
            "status": status,
            "offset": offset,
            "count": count,
        }
        response = RequestBody.req(self, key=self.apikey, method="getChecks", data=params)
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
            if len(response["result"]["items"]) > 0:
                if check_ids and isinstance(check_ids, int):
                    return Check(**response["result"]["items"][0])
            return [Check(**check) for check in response["result"]["items"]]
    def getBalance(self)-> List[Balance]:
        response = RequestBody.req(self, key=self.apikey, method="getBalance")
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
                return [Balance(**balance) for balance in response["result"]]
      
    def getExchangeRates(self) -> List[ExchangeRate]:
        response = RequestBody.req(self, key=self.apikey, method="getExchangeRates")
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
                return [ExchangeRate(**rate) for rate in response["result"]]

    def getCurrencies(self) -> List[Currency]:
        response = RequestBody.req(self, key=self.apikey, method="getCurrencies")
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
                return [Currency(**currency) for currency in response["result"]]

    def getStats(
        self,
        start_at: Optional[Union[datetime, str]] = None,
        end_at: Optional[Union[datetime, str]] = None,
    ) -> AppStats:
        params = {
            "start_at": start_at,
            "end_at": end_at
        }
        response = RequestBody.req(self, key=self.apikey, method="getStats", data=params)
        if isinstance(response, str):
                logger.error(response)
                return False
        else:
                return AppStats(**response["result"])
    def getAmountByFiat(
        self, summ: Union[int, float], asset: Union[Assets, str], target: str
    ) -> Union[int, float]:
        rates = self.getExchangeRates()
        rate = getRate(source=asset, target=target, rates=rates)
        fiatSumm = getRateSumm(summ=summ, rate=rate)
        return fiatSumm