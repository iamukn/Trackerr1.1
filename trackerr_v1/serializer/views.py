from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Person
from .serializer import PersonSerializer
import io
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
from django.http import HttpResponse

person = {'name': "Ukaegbu", 'age': 53, 'color': 'blue'}

class PersonView(APIView):
    permissions_class = [AllowAny]
    
    def get(self, request, *arg, **kwargs):
        global person
        serializer = PersonSerializer(Person.objects.all(), many=True)
        serializer.data
        data = JSONRenderer().render(serializer.data)
        return HttpResponse(data, content_type='application/json')

    def post(self, request, *arg, **kwargs):
        print(request.data)
       # data = json.dumps(request.data)
       # data = {'name': request.data.get('name'), 'age': request.data.get('age'), 'color': request.data.get('color')}
    
        d = json.dumps(request.data).encode('utf-8')
        d = io.BytesIO(d)    
        new_d = JSONParser().parse(d)

        ser = PersonSerializer(data=new_d)
        if ser.is_valid() and ser.validate(request.data):
            ser.save()

            return Response('200')
        
        

        return Response('400')
