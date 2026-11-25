def restructure_transaction(data):
    data = data.order_by('-paid_at')
    yearly = {
            "2026": []
            }
    for payment in data:
        date_paid = payment.paid_at
        if date_paid:
            year = date_paid.year
            month = payment.paid_at.strftime('%B').lower()
            payment_record = {
                "amount": payment.amount,
                "date_paid": payment.paid_at.strftime('%Y-%m-%d'),
                "time_paid": payment.paid_at.strftime('%H:%M:%S'),
                "payment_channel": 'bank transfer' if payment.payment_channel == 'bank_transfer' else 'mobile money' if payment.payment_channel == 'mobile_money' else payment.payment_channel,
                "currency": payment.currency
                    }
            if yearly.get(year):
                if yearly.get(year).get(month):
                    yearly[year][month].append(payment_record)
                else:
                    yearly[year][month] = [payment_record]

            else:
                yearly[year] ={
                        month:
                        [
                            payment_record
                        ]
                        }
    return [yearly]
