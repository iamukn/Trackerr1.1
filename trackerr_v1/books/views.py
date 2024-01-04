from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializer import BooksSerializer, AuthorSerializer
from .models import Books, Author

class BooksViewSet(ModelViewSet):
    serializer_class = BooksSerializer

    def get_queryset(self):

        data = Books.objects.all()
        return data

    def create(self, request, *args, **kwargs):
        req = request.data


        new_author = Author.objects.create(name=req['name'], is_softcopy=req['is_softcopy'])
        new_author.save()

        new_book = Books.objects.create(title=req['title'], isbn=req['isbn'], chapter=req['chapter'], relationship=new_author)
        new_book.save()

        serializer = BooksSerializer(new_book)

        return Response(serializer.data)



class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer

    def get_queryset(self):

        author = Authors.objects.all()

        return author
