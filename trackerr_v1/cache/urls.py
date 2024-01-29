from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('cache/',views.PostView.as_view(), name='cache'),
    path('caches/',views.PaginateView.as_view(), name='caches'),
    path('reverse/',views.reverser, name='reverser'),
        ]


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'csv'])
