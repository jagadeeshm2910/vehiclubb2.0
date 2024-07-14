from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Vehicle, PublishRide, PassengerRide, UserProfile


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='userprofile.phone_number')

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone_number']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        profile_data = validated_data.pop('userprofile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user
    
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['user', 'id', 'vehicle_type', 'car_color', 'car_brand', 'car_plate_number']

class PublishRideSerializer(serializers.ModelSerializer):
    rider = serializers.SerializerMethodField()
    rider_phone_number = serializers.SerializerMethodField()
    

    class Meta:
        model = PublishRide
        fields = ['id', 'source', 'destination', 'ride_date', 'ride_time', 'seats_available', 'car_plate_number', 'rider_flag', 'selected_route', 'rider', 'rider_phone_number']

    def get_rider(self, obj):
        return obj.car_plate_number.user.username
    
    def get_rider_phone_number(self, obj):
        return obj.car_plate_number.user.userprofile.phone_number

class PassengerRideSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    phone_number = serializers.CharField(source='user.userprofile.phone_number', required=False)

    class Meta:
        model = PassengerRide
        fields = ['id', 'user', 'username', 'source', 'destination', 'date', 'time', 'passenger_ride_flag', 'selected_ride', 'phone_number']