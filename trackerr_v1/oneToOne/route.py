from django.urls import path
from . import views as dept_view
urlpatterns = [
    path('dept_get/', dept_view.Dept_Reg.as_view(), name='dept_get'),
        ]
