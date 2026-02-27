from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


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
    # latitude:  max_digits=9  allows ±90.000000  (2 integer digits + 6 decimal)
    # longitude: max_digits=10 allows ±180.000000 (3 integer digits + 6 decimal)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'created_at']
        constraints = [
            models.CheckConstraint(
                condition=Q(latitude__isnull=True) | Q(latitude__gte=-90) & Q(latitude__lte=90),
                name='latitude_range',
            ),
            models.CheckConstraint(
                condition=Q(longitude__isnull=True) | Q(longitude__gte=-180) & Q(longitude__lte=180),
                name='longitude_range',
            ),
        ]

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
        constraints = [
            # Ensures at most one image per destination can be marked as primary.
            models.UniqueConstraint(
                fields=['destination'],
                condition=Q(is_primary=True),
                name='unique_primary_image_per_destination',
            )
        ]

    def clean(self):
        super().clean()
        if self.is_primary:
            qs = DestinationImage.objects.filter(destination=self.destination, is_primary=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    {'is_primary': 'Another image for this destination is already marked as primary.'}
                )

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
            ),
            # Prevents nonsensical "distance from X to X" records.
            models.CheckConstraint(
                condition=~Q(from_destination=F('to_destination')),
                name='no_self_referencing_distance',
            ),
        ]

    def clean(self):
        super().clean()
        # Validate that both destinations belong to the same trip.
        # CheckConstraint cannot enforce cross-row/cross-table rules in SQLite,
        # so this is enforced at the model validation layer instead.
        if (
            self.from_destination_id
            and self.to_destination_id
            and self.from_destination_id == self.to_destination_id
        ):
            raise ValidationError('A destination cannot have a distance to itself.')

        if self.from_destination_id and self.to_destination_id:
            from_trip = self.from_destination.trip_id
            to_trip = self.to_destination.trip_id
            if from_trip != to_trip:
                raise ValidationError(
                    'Both destinations must belong to the same trip.'
                )

    def __str__(self):
        return f'{self.from_destination} → {self.to_destination}'
