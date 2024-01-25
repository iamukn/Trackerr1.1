from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from random import randint

from .models import Phone
from .serializer import PhoneSerializer

class PostView(APIView):
    # Cache page for the requested url
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        queryset = Phone.objects.all()
        ser = PhoneSerializer(queryset, many=True)
        data = [phones for phones in ser.data]

        return Response(data)
