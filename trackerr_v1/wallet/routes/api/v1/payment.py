from django.shortcuts import get_object_or_404, Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from business.views.business_owner_permission import IsBusinessOwner
from wallet.payment_logic.payment_logic import initialize_payment
from wallet.serializer import PaymentSerializer, WalletSerializer
from wallet.models import Payment, Wallet
from wallet.utils.verify import validate_idempotency_key
from decimal import Decimal
from user.models import User
from django.db import transaction
from wallet.utils.convert_amount import actual_amount_paid
from business.views.business_owner_permission import IsBusinessOwner



class PaymentDeposit(APIView):
    """
      Handles Deposit for business owners
    """
    permission_classes = [IsBusinessOwner,]


    def post(self, request, *args, **kwargs):
        email = request.user.email
        amount = request.data.get('amount')
        idempotency_key = request.headers.get('Idempotency-Key')

        if not idempotency_key and \
           not email and not amount:
               return Response({'msg': 'error', 'details': "email, amount payload and idempotency key in the header is required"}, status=status.HTTP_400_BAD_REQUEST)


        if not idempotency_key:
            return Response({'msg': 'error', 'details': "idempotency key in the header is required"}, status=status.HTTP_400_BAD_REQUEST)


        if not email:
            return Response({'msg': 'error', 'details': "email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not amount:
            return Response({'msg': 'error', 'details': "amount is required"}, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            # confirm if idempotency key already exist and status is pending,
            #if it does send the existing authorization url 
            key_exist = validate_idempotency_key(idempotency_key)

            if key_exist:
                return Response({'msg': 'success', 'authorization_url': key_exist}, status=status.HTTP_200_OK)
            payment_initialized = initialize_payment(email=email, amount=amount, country=request.user.country)
            
            data = {
                'email' : email.lower(),
                'amount': amount,
                'vat': float(payment_initialized.get('vat')),
                'reference_number': payment_initialized.get('data').get('reference'),
                'authorization_url': payment_initialized.get('data').get('authorization_url'),
                'idempotency_key': idempotency_key
                    }

            payment_serializer = PaymentSerializer(data=data)
            if payment_serializer.is_valid():
                # save the payment
                payment_serializer.save()
                return Response({'msg': 'success', 'autorization_url': payment_initialized.get('data').get('authorization_url')}, status=status.HTTP_200_OK)
            return Response({'msg': 'error', 'details': payment_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise(e)
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Payment Webhook
class PaymentWebhook(APIView):
    permission_classes = [AllowAny,]


    def get_queryset(self, reference: str):
        payment = Payment.objects.filter(reference_number=reference, status='pending').first()
        return payment


    def get_wallet(self, customer_email: str):
        owner = User.objects.get(email=customer_email)
        wallet = Wallet.objects.select_for_update().get(owner=owner)
        return wallet

    def update_balance(self, wallet, amount, vat):
        if amount > 0:
            amount = Decimal(str(amount))
            actual_amount = actual_amount_paid(amount=amount, vat=vat, country=wallet.owner.country)
            current_bal = Decimal(str(wallet.balance))
            new_amount = current_bal + actual_amount
            wallet.balance = new_amount
            wallet.save()


    def post(self,request, *args, **kwargs ):

        data = request.data
        if data:
            base_data = data.get('data')
            # do nothing if it's a test domain
            if not base_data.get('domain') == 'test':
                return Response(status=status.HTTP_204_NO_CONTENT)

            # get payment object using reference
            authorization = base_data.get('authorization')
            payment_obj = self.get_queryset(base_data.get('reference'))

            deposit_status = base_data.get('status')
            #fetch owner
            try:
                with transaction.atomic():
                    owner_email = base_data.get('customer').get('email')
                    owner = self.get_wallet(owner_email)

                    update_wallet = self.update_balance(wallet=owner, amount=base_data.get('amount'), vat=payment_obj.vat)

                    if payment_obj:

                        # update the amount in the wallet

                        payload = {
                            'status': deposit_status,
                            'payment_channel': base_data.get('channel'),
                            'ip_address': base_data.get('ip_address'),
                            'sender_name': authorization.get('sender_name'),
                            'sender_bank': authorization.get('sender_bank'),
                            'sender_account_number': authorization.get('sender_bank_account_number'),
                            'sender_country':  authorization.get('sender_country'),
                            'sender_narration': authorization.get('sender_narration'),
                            'card_type': authorization.get('card_type'),
                            'last4': authorization.get('last4'),
                            'exp_month': authorization.get('exp_month'),
                            'exp_year': authorization.get('exp_year'),
                            'account_name': authorization.get('account_name'),
                            'country_code': authorization.get('country_code'),
                            'created_at': base_data.get('created_at'),
                            'paid_at': base_data.get('paid_at'),
                                }

                        if base_data.get('channel') == 'bank':
                            payload['sender_bank'] = authorization.get('bank')

                        serializer = PaymentSerializer(payment_obj, data=payload, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print('Error:', serializer.errors)
                    return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                raise e
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

