from celery import shared_task

@shared_task(bind=True, name='verify_payment')
def verify_payment(self,):
    print('Done')
