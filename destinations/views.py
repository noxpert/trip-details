from django.db.models import Count
from django.views.generic import ListView

from .models import Trip


class TripListView(ListView):
    model = Trip
    template_name = 'destinations/trip_list.html'

    def get_queryset(self):
        return Trip.objects.annotate(destination_count=Count('destinations')).order_by('-created_at')
