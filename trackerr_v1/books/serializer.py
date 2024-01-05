from .models import Books, Author
from rest_framework.serializers import ModelSerializer


class BooksSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = ['id', 'title', 'isbn', 'chapter', 'relationship',]
        depth = 1

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = [ 'name', 'is_softcopy']
        depth = 1
