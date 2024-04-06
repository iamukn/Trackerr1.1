from django.urls import path
from .routes import logistics_users_count as logistics_count
urlpatterns = [
    path('logistics-owners-count/', logistics_count.Logistics_owners_count.as_view(), name='logistics-count'),
        ]
