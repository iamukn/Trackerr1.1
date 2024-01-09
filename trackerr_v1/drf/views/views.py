from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf.serializer import BookSerializer
from drf.models import Books
from rest_framework import authentication, permissions

@api_view(['GET'])
def home(request):
    req = request.query_params
    print(dir(permissions))
#    print(request.DJANGO_SETTINGS_MODULE)
    if 'author' and 'message' in req:
        author = req.get('author')
        message = req.get('message')

        data = Books.objects.filter(author=author,message=message)
        serializer = BookSerializer(data, many=True)
        print('Data outside %s' % data)
        if serializer.data:
            print(data)
            return Response('Found')

        return Response('Not found')
    res = Response('Wahala dey')
    return res

# Create your views here.


