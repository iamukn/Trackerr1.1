from django.shortcuts import render
from rest_framework.response import Response
from .models import Business_owner
from .serializers import Business_ownerSerializer
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer

# Create your views here.
@api_view(['GET'])
#@renderer_classes([JSONRenderer])
def home(request):
    query_set = Business_owner.objects.all()
    serializer = Business_ownerSerializer(query_set, many=True)
    return Response(serializer.data)
