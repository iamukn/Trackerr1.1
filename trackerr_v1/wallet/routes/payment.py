from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class PaymentWebhook(APIView):
    permission_classes = [AllowAny,]

    def post(self,request, *args, **kwargs ):

        print(request.data)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
