## **Module CryptoBot API(non-official)**
**Docs:** https://help.crypt.bot/crypto-pay-api

**Install**
``` bash
pip install TeleCryptoBot
```

**Basic Methods**

``` python
import TeleCryptoBot

crypto = TeleCryptoBot.TeleCryptoBot("0000:qwertyuiop")

info_profile = crypto.getMe()
balance = crypto.getBalance()

print(info_profile, balance, sep='\n')
```

**Create and Delete Invoice**
``` python
import TeleCryptoBot

crypto = TeleCryptoBot.TeleCryptoBot("0000:qwertyuiop")
#create invoice
invoice = crypto.createInvoice(asset="USDT", amount=1.0)
print(invoice.invoice_id)
# delete invoice
delete = crypto.deleteInvoice(invoice_id=invoice.invoice_id)
```

**Create and Delete Check**
``` python
import TeleCryptoBot

crypto = TeleCryptoBot.TeleCryptoBot("0000:qwertyuiop")
#create invoice
check = crypto.createCheck(asset="USDT", amount=1.0, pin_to_username="durov")
print(check.check_id)
# delete invoice
delete = crypto.deleteCheck(check_id.check.check_id)
```
**Get Amount By Fiat**
``` python
import TeleCryptoBot

crypto = TeleCryptoBot.TeleCryptoBot("0000:qwertyuiop")
# Get amount in crypto by fiat summ
amount = crypto.getAmountByFiat(summ=13, asset='TON', target='USD')
invoice = crypto.createInvoice(asset='TON', amount=amount)
print(invoice.bot_invoice_url)
```
