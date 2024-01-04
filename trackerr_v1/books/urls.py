from .views import BooksViewSet, AuthorViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('books', BooksViewSet, basename= 'books')
router.register('author', AuthorViewSet, basename= 'author')



urlpatterns = (
    path('', include(router.urls)),

)
