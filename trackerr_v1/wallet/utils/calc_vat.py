from decimal import Decimal
""" calculate value added tax per deposit """

def calc_vat(amount, country):
    amount = amount / 100
    
    if country == 'ghana':
        # 3.9% charge for other countries as vat
        vat = (Decimal(amount) * Decimal("0.02"))


    else:
        if amount >= 2500:
            vat = (Decimal(amount) * Decimal("0.015"))
            if vat > Decimal(2000):
                vat = Decimal(2000)
            else:
                vat += Decimal(100)
        else:
            vat = (Decimal(amount) * Decimal("0.015"))
    return vat * 100
