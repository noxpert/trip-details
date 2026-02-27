from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import TripForm
from .models import Destination, Trip


class TripListView(ListView):
    model = Trip
    template_name = 'destinations/trip_list.html'

    def get_queryset(self):
        return Trip.objects.annotate(destination_count=Count('destinations')).order_by('-created_at')


class TripCreateView(CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'destinations/trip_form.html'

    def get_success_url(self):
        return reverse_lazy('destinations:trip_detail', kwargs={'pk': self.object.pk})


class TripDetailView(DetailView):
    model = Trip
    template_name = 'destinations/trip_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinations'] = (
            Destination.objects.filter(trip=self.object)
            .prefetch_related('images')
            .order_by('sort_order', 'created_at')
        )
        return context


class TripUpdateView(UpdateView):
    model = Trip
    form_class = TripForm
    template_name = 'destinations/trip_form.html'

    def get_success_url(self):
        return reverse_lazy('destinations:trip_detail', kwargs={'pk': self.object.pk})


class TripDeleteView(DeleteView):
    model = Trip
    template_name = 'destinations/trip_confirm_delete.html'
    success_url = reverse_lazy('destinations:trip_list')

