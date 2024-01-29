from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from random import randint

from rest_framework.pagination import PageNumberPagination

from .models import Phone
from .serializer import PhoneSerializer


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 3


class PaginateView(generics.ListAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    pagination_class = SmallResultsSetPagination

class PostView(APIView):
    pagination_class = SmallResultsSetPagination
    # Cache page for the requested url
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        paginator = self.pagination_class()
        queryset = Phone.objects.all()
        page = paginator.paginate_queryset(queryset, request, view=self)
        ser = PhoneSerializer(page, many=True)
        return Response(ser.data)

@api_view(['GET'])
def reverser(request):
    url1 = reverse('cache', request=request)
    url2 = reverse('caches', request=request)

    data = "{} and {}".format(url1, url2)

    return Response(data)

