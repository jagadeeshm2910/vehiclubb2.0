from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login, name='login'),
    path('postvehicle/', views.create_vehicle, name='create_vehicle'),
    path('getvehicle/', views.get_vehicle, name='get_vehicle'),
    path('publish_ride/', views.publish_ride, name='publish_ride'),
    path('get_published_rides/', views.get_published_rides, name='get_published_rides'),
    path('create_passenger_ride/', views.create_passenger_ride, name='create_passenger_ride'),
    path('get_passenger_rides/', views.get_passenger_rides, name='get_passenger_rides'),
    path('update_rider_flag/<int:ride_id>/', views.update_rider_flag, name='update_rider_flag'),
    path('update_passenger_ride_flag/<int:ride_id>/', views.update_passenger_ride_flag, name='update_passenger_ride_flag'),
    path('get_passengers_for_ride/<int:ride_id>/', views.get_passengers_for_ride, name='get_passengers_for_ride'),
    path('get_all_published_rides/', views.get_all_published_rides, name='get_all_published_rides'),
]

