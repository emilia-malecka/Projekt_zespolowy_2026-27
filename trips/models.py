from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"

class TripPoint(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='points')
    name = models.CharField(max_length=200) # np. "Berlin"
    order = models.PositiveIntegerField()   # Kolejność: 1, 2, 3...
    latitude = models.FloatField()          # Szerokość geograficzna
    longitude = models.FloatField()         # Długość geograficzna
    country_code = models.CharField(max_length=2, blank=True, null=True) # Kod państwa, np. "DE"

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.name} (w {self.trip.title})"


class TripSegment(models.Model):
    TRANSPORT_CHOICES = [
        ('CAR', 'Samochód'),
        ('PLANE', 'Samolot'),
        ('TRAIN', 'Pociąg'),
        ('OTHER', 'Inne'),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='segments')
    start_point = models.ForeignKey(TripPoint, on_delete=models.CASCADE, related_name='segment_starts')
    end_point = models.ForeignKey(TripPoint, on_delete=models.CASCADE, related_name='segment_ends')
    
    transport_mode = models.CharField(max_length=10, choices=TRANSPORT_CHOICES, default='OTHER')
    distance_km = models.FloatField(default=0.0)
    
    geometry = models.JSONField(blank=True, null=True) 

    def __str__(self):
        return f"{self.start_point.name} -> {self.end_point.name} [{self.get_transport_mode_display()}]"