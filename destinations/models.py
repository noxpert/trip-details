from django.db import models


class Trip(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Destination(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='destinations')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=500, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return self.name


class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='destinations/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=300, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        if self.caption:
            return self.caption
        return f'Image for {self.destination.name}'


class DestinationDistance(models.Model):
    from_destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='distances_from'
    )
    to_destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='distances_to'
    )
    haversine_distance_km = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    driving_distance_km = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    driving_duration_minutes = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    directions_json = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['from_destination', 'to_destination']
        constraints = [
            models.UniqueConstraint(
                fields=['from_destination', 'to_destination'],
                name='unique_destination_pair',
            )
        ]

    def __str__(self):
        return f'{self.from_destination} → {self.to_destination}'
