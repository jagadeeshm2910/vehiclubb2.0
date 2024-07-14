from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

CAR_COLOR_CHOICES = [
    ('red', 'Red'),
    ('blue', 'Blue'),
    ('black', 'Black'),
    ('white', 'White'),
    ('silver', 'Silver'),
]

VEHICLE_TYPE_CHOICES = [
    ('two_wheeler', 'Two-wheeler'),
    ('four_wheeler', 'Four-wheeler'),
]

CAR_BRAND_CHOICES = [
    ('toyota', 'Toyota'),
    ('honda', 'Honda'),
    ('ford', 'Ford'),
    ('chevrolet', 'Chevrolet'),
    ('nissan', 'Nissan'),
    ('tata', 'Tata'),
    ('maruti_suzuki', 'Maruti Suzuki'),
    ('mahindra', 'Mahindra'),
    ('hyundai', 'Hyundai'),
    ('kia', 'Kia'),
    ('volkswagen', 'Volkswagen'),
    ('renault', 'Renault'),
    ('citroen', 'Citroen'),
    ('skoda', 'Skoda'),
    ('isuzu', 'Isuzu')
    # Add more brands as needed
]


class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    vehicle_type = models.CharField(max_length=100, choices=VEHICLE_TYPE_CHOICES, default='four_wheeler')
    car_color = models.CharField(max_length=100, choices=CAR_COLOR_CHOICES)
    car_brand = models.CharField(max_length=100, choices=CAR_BRAND_CHOICES)
    car_plate_number = models.CharField(max_length=100)
    

    def __str__(self):
        return self.car_plate_number
    

# create a model for the Rider with fields: name, phone_number, email, location, car_color, car_brand, car_plate_number, car_capacity

class PublishRide(models.Model):
    RIDE_STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    ride_date = models.DateField()
    ride_time = models.TimeField()
    seats_available = models.IntegerField()
    selected_route = ArrayField(
        ArrayField(
            models.FloatField(
                blank=True,
                null=True
            ),
            size=2
        ),
        size=2000
    )
    car_plate_number = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    rider_flag = models.CharField(max_length=10, choices=RIDE_STATUS_CHOICES, default='upcoming')

    def save(self, *args, **kwargs):
        if self.pk is not None:  # if the instance already exists in the database
            orig = PublishRide.objects.get(pk=self.pk)
            if orig.rider_flag == 'cancelled' and self.rider_flag != 'cancelled':
                raise ValidationError('You cannot change the rider flag from cancelled to other states.')
            if orig.rider_flag != 'cancelled' and self.rider_flag == 'cancelled':
                PassengerRide.objects.filter(selected_ride=self).update(passenger_ride_flag='cancelled')
        if self.pk is None:  # if the instance is not yet saved in the database
            existing_rides = PublishRide.objects.filter(
                car_plate_number=self.car_plate_number,
                ride_date=self.ride_date,
                source=self.source,
                rider_flag__in=['upcoming', 'active', 'completed']
            )
            if existing_rides.exists():
                raise ValidationError('You already have a ride with the same date and source that is not cancelled.')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ride from {self.source} to {self.destination} on {self.ride_date} at {self.ride_time}"
    

class PassengerRide(models.Model):
    PASSENGER_RIDE_STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('denied', 'Denied'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    passenger_ride_flag = models.CharField(max_length=10, choices=PASSENGER_RIDE_STATUS_CHOICES, default='requested')
    selected_ride = models.ForeignKey(PublishRide, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk is not None:  # if the instance already exists in the database
            orig = PassengerRide.objects.get(pk=self.pk)
            if orig.passenger_ride_flag in ['cancelled', 'denied'] and self.passenger_ride_flag != orig.passenger_ride_flag:
                raise ValidationError('Cannot change the ride flag from cancelled or denied to other states.')
            if orig.passenger_ride_flag == 'accepted' and self.passenger_ride_flag == 'cancelled':
                self.selected_ride.seats_available += 1
                self.selected_ride.save()
            elif orig.passenger_ride_flag != 'accepted' and self.passenger_ride_flag == 'accepted':
                self.selected_ride.seats_available -= 1
                self.selected_ride.save()
        if self.pk is None:  # if the instance is not yet saved in the database
            existing_rides = PassengerRide.objects.filter(
                user=self.user,
                date=self.date,
                source=self.source,
                passenger_ride_flag__in=['requested', 'accepted', 'active', 'completed']
            ).exclude(
            passenger_ride_flag__in=['cancelled', 'denied']
            )
            if existing_rides.exists():
                raise ValidationError('You already have a ride with the same date and source that is not cancelled or denied.')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Passenger Ride from {self.source} to {self.destination} on {self.date} at {self.time}"