#!/usr/bin/python3
from .models import Tracking_info
from rest_framework.serializers import ModelSerializer
from tracking_information.models import Tracking_info, GeoLocationData
from tracking_information.utils.distance import calc_distance
from tracking_information.utils.calc_eta import calculate_eta as calc_eta
from tracking_information.utils.track_gen import tracking_number_generate
from django.db import IntegrityError

""" A serializer class for the tracking_information """

class Tracking_infoSerializer(ModelSerializer):
    
    class Meta:
        model = Tracking_info
        fields = '__all__'



    def create(self, validated_data):
        max_attempt = 5
        for attempt in range(max_attempt):
            validated_data['parcel_number'] = tracking_number_generate()
            try:
                return super().create(validated_data)
            except IntegrityError:
                if attempt == max_attempts - 1:
                    raise IntegrityError

    def to_representation(self, instance):

        # calc distance between origin and dest

        if not instance.business_owner_lat or not instance.business_owner_lng:
             dist = calc_distance(
                     float(instance.destination_lat),
                     float(instance.destination_lng),
                     float(instance.destination_lat),
                     float(instance.destination_lng),
                    )
        else:
            dist = calc_distance(
                float(instance.business_owner_lat),
                float(instance.business_owner_lng),
                float(instance.destination_lat),
                float(instance.destination_lng),
                    )

        eta = calc_eta(dist, 30)

        data = super().to_representation(instance)

        data['dist'] = f"{dist:.2f}km".strip()
        data['eta'] = eta

        return data


class GeoLocationSerializer(ModelSerializer):
    class Meta:
        model = GeoLocationData
        fields = '__all__'
