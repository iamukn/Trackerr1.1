from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view



@api_view(['GET'])
def home(request):
    print(request.query_params.dict())
    return Response('Hello World')

# Create your views here.


