from rest_framework import serializers
from .models import Person
from rest_framework.renderers import JSONRenderer

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=55)
    age = serializers.IntegerField()
    color = serializers.CharField()


    def create(self, validated_data):
        return Person.objects.create(**validated_data)

    def update(self, instance, validate_data):
        instance.name = validate_data.get('name', instance.name)
        instance.age = validate_data.get('age', instance.age)
        instance.color = validate_data.get('color', instance.color)
        return instance 

    def validate_color(self, data):
        if len(data) > 5 :
            return data
        raise serializers.ValidationError('color must be of 5 character')
