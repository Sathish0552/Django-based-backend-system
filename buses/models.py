import random
from django.db import models

class Bus(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance')
    ]

    name = models.CharField(max_length=100, unique=True)
    route_number = models.CharField(max_length=20, unique=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.name} - Route {self.route_number}"

    def save(self, *args, **kwargs):
        # Call the original save method to save the bus data
        super().save(*args, **kwargs)

        # Generate random coordinates after the bus is saved
        if not self.locations.exists():  # Check if there are no locations yet
            latitude = round(random.uniform(-90, 90), 6)  # Random latitude between -90 and 90
            longitude = round(random.uniform(-180, 180), 6)  # Random longitude between -180 and 180

            # Create a BusLocation object with the random coordinates
            BusLocation.objects.create(bus=self, latitude=latitude, longitude=longitude)


class BusLocation(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bus: {self.bus.name} | Location: ({self.latitude}, {self.longitude})"
