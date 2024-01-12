from drf.models import Books
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf.serializer import UsersSerializer, BookSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer

class MyViewSet(ViewSet):
    parser_class = [JSONParser]
    def list(self, request):
        data = Books.objects.all()
        serializer = BookSerializer(data, many=True)

        return Response(serializer.data)

    def create(self, request):

        data = request.data
        serializer = BookSerializer(data=data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response('Bad request', status=400)
    
    def update(self, request, pk=None):
        user = Books.objects.get(pk=pk)
        serializer = BookSerializer(user, data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response('Put Update failed')

    def retrieve(self, request, pk=None):
        data = Books.objects.all()
        print(request.data)
        data = get_object_or_404(data, id=pk)
        serializer =BookSerializer(data, many=False)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        user =  get_object_or_404(Books, pk=pk)
        serializer = BookSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        data = Books.objects.all()
        data = get_object_or_404(data, pk=pk)
        serializer = BookSerializer(data, many=False)
        data.delete()

        return Response(serializer.data)


