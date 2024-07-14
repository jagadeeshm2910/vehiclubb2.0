from django.shortcuts import render

# Create your views here.
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, VehicleSerializer, PublishRideSerializer, PassengerRideSerializer
from .models import Vehicle, PublishRide, PassengerRide

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return Response({'message': 'Successful login'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid login'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vehicle(request):
    data = request.data.copy()
    data['user'] = request.user.id
    serializer = VehicleSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vehicle(request):
    try:
        vehicle = Vehicle.objects.filter(user=request.user)
        serializer = VehicleSerializer(vehicle, many=True)
        return Response(serializer.data)
    except Vehicle.DoesNotExist:
        return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def publish_ride(request):
    user_vehicles = Vehicle.objects.filter(user=request.user)
    if not user_vehicles.exists():
        return Response({'error': 'No vehicles associated with this user.'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = PublishRideSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_published_rides(request):
    user_vehicles = Vehicle.objects.filter(user=request.user)
    published_rides = PublishRide.objects.filter(car_plate_number__in=user_vehicles)
    serializer = PublishRideSerializer(published_rides, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_passenger_ride(request):
    print(request.data)
    serializer = PassengerRideSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            print(e)
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_passenger_rides(request):
    rides = PassengerRide.objects.filter(user=request.user)
    serializer = PassengerRideSerializer(rides, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_rider_flag(request, ride_id):
    try:
        ride = PublishRide.objects.get(id=ride_id)
    except PublishRide.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if ride.car_plate_number.user != request.user:
        return Response({"error": "You are not authorized to update this ride"}, status=status.HTTP_403_FORBIDDEN)

    if 'rider_flag' in request.data:
        ride.rider_flag = request.data['rider_flag']
        ride.save()
        return Response(PublishRideSerializer(ride).data)
    else:
        return Response({"error": "Missing rider_flag in request"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_passenger_ride_flag(request, ride_id):
    try:
        ride = PassengerRide.objects.get(id=ride_id)
    except PassengerRide.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if 'passenger_ride_flag' in request.data:
        ride.passenger_ride_flag = request.data['passenger_ride_flag']
        ride.save()
        return Response(PassengerRideSerializer(ride).data)
    else:
        return Response({"error": "Missing passenger_ride_flag in request"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_passengers_for_ride(request, ride_id):
    try:
        ride = PublishRide.objects.get(id=ride_id)
    except PublishRide.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    passengers = PassengerRide.objects.filter(selected_ride=ride)
    serializer = PassengerRideSerializer(passengers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_published_rides(request):
    published_rides = PublishRide.objects.all()
    serializer = PublishRideSerializer(published_rides, many=True)
    return Response(serializer.data)