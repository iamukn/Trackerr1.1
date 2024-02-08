from django.urls import path
from . import views as dept_view
url_patterns = [
    path('dept_get/', dept_view.Dept_Reg.as_view(), name='dept_get'),
        ]
