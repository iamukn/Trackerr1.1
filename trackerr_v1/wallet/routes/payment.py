from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from business.views.business_owner_permission import IsBusinessOwner
from wallet.payment_logic.payment_logic import initialize_payment



class PaymentDeposit(APIView):
    """
      Handles Deposit for business owners
    """
    permission_classes = [AllowAny,]


    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        amount = request.data.get('amount')

        try:
            payment_initialized = initialize_payment(email, amount, 'NGN')

            # Add payment info to DB USING Transactions
            #add_payment_info_to_db(payment_initialized, email, amount, 'NGN')
            return Response({'msg': 'success', 'autorization_url': payment_initialized.get('data').get('authorization_url')}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentWebhook(APIView):
    permission_classes = [AllowAny,]

    def post(self,request, *args, **kwargs ):

        print(request.data)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
