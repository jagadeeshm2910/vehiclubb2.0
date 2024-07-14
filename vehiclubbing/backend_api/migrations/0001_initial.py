# Generated by Django 5.0.6 on 2024-05-27 13:48

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PublishRide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('ride_date', models.DateField()),
                ('ride_time', models.TimeField()),
                ('seats_available', models.IntegerField()),
                ('selected_route', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), size=2), size=2000)),
                ('rider_flag', models.CharField(choices=[('upcoming', 'Upcoming'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='upcoming', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PassengerRide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('passenger_ride_flag', models.CharField(choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('denied', 'Denied')], default='requested', max_length=10)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('selected_ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.publishride')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(choices=[('two_wheeler', 'Two-wheeler'), ('four_wheeler', 'Four-wheeler')], default='four_wheeler', max_length=100)),
                ('car_color', models.CharField(choices=[('red', 'Red'), ('blue', 'Blue'), ('black', 'Black'), ('white', 'White'), ('silver', 'Silver')], max_length=100)),
                ('car_brand', models.CharField(choices=[('toyota', 'Toyota'), ('honda', 'Honda'), ('ford', 'Ford'), ('chevrolet', 'Chevrolet'), ('nissan', 'Nissan'), ('tata', 'Tata'), ('maruti_suzuki', 'Maruti Suzuki'), ('mahindra', 'Mahindra'), ('hyundai', 'Hyundai'), ('kia', 'Kia'), ('volkswagen', 'Volkswagen'), ('renault', 'Renault'), ('citroen', 'Citroen'), ('skoda', 'Skoda'), ('isuzu', 'Isuzu')], max_length=100)),
                ('car_plate_number', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='publishride',
            name='car_plate_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_api.vehicle'),
        ),
    ]
