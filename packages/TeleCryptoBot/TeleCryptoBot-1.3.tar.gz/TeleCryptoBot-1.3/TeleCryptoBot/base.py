from strenum import StrEnum

class Assets(StrEnum):
    """Crypto Assets"""

    BTC = "BTC"
    TON = "TON"
    ETH = "ETH"
    USDT = "USDT"
    USDC = "USDC"
    BNB = "BNB"
    TRX = "TRX"
    LTC = "LTC"

    @classmethod
    def values(cls):
        return list(map(lambda asset: asset.value, cls))


class PaidButtons(StrEnum):
    """Names for Paid Buttons"""

    VIEW_ITEM = "viewItem"
    OPEN_CHANNEL = "openChannel"
    OPEN_BOT = "openBot"
    CALLBACK = "callback"


class InvoiceStatus(StrEnum):
    """Invoice status"""

    ACTIVE = "active"
    PAID = "paid"
    EXPIRED = "expired"


class CheckStatus(StrEnum):
    """Check status"""

    ACTIVE = "active"
    ACTIVATED = "activated"


class CurrencyType(StrEnum):
    """Currency type"""

    CRYPTO = "crypto"
    FIAT = "fiat"