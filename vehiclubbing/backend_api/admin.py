from django.contrib import admin

# Register your models here.
from .models import Vehicle, PublishRide, PassengerRide

admin.site.register(Vehicle)
admin.site.register(PublishRide)
admin.site.register(PassengerRide)

