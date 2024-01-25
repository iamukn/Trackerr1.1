from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from random import randint

class PostView(APIView):
    # Cache page for the requested url
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        name = ['dan', 'david']
        content = {
            "title": data[randint(0, 1)],
            "body": "Post content",
        }
        return Response(content)
