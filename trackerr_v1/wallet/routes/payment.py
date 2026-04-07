from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from business.views.business_owner_permission import IsBusinessOwner
from wallet.payment_logic.payment_logic import initialize_payment
from wallet.serializer import PaymentSerializer
from wallet.utils.verify import validate_idempotency_key



class PaymentDeposit(APIView):
    """
      Handles Deposit for business owners
    """
    permission_classes = [AllowAny,]


    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
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
            payment_initialized = initialize_payment(email, amount, 'NGN')
            
            data = {
                'email' : email.lower(),
                'amount': amount,
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
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentWebhook(APIView):
    permission_classes = [AllowAny,]

    def post(self,request, *args, **kwargs ):

        print(request.data)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
