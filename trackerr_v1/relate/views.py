from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class Home(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return HttpResponse("Welcome to Home")

