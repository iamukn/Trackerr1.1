from celery import shared_task
import os
from requests.exceptions import ConnectionError, Timeout, RequestException

def confirm_payment() -> None:
    # fetch payments that are pending

    from wallet.models import Payment
    all_payments = Payment.objects.filter(status='pending', reference_number__isnull=False)
    if not all_payments:
        print('No pending payment')
        return
    import requests

    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")
    api_key = os.environ.get('PAYSTACK_SECRET_KEY')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
            }

    for payment in all_payments:
        url = f"https://api.paystack.co/transaction/verify/{payment.reference_number}"
        # call to verify
        try:
            res = requests.get(url, headers=headers)

            if not res.status_code == 200:
                return

            res_data = res.json()
            data = res_data.get('data')

            if not data.get('domain') == 'test':
                return

            status = data.get('status')

            if status in ['abandoned', 'failed', 'reversed']:
                payment.status = status
                payment.save()

            elif status in ['pending', 'ongoing', 'processing', 'queued']:
                continue

            else:
                requests.post(f'{APP_BASE_URL}/api/v1/payments/webhook', json=res_data)

        except ConnectionError as e:
            # DNS failure, refused connection, etc.
            print(f"Connection error: {e}")
            # Optionally retry later or log for monitoring
            return
        except Exception as e:
            print('Error::', e)
            return


@shared_task(bind=True, name='verify_pending_payment')
def pending_payment(self,):
    confirm_payment()
