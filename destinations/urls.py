from django.urls import path

from . import views

app_name = 'destinations'

urlpatterns = [
    # Trip list (home)
    path('', views.TripListView.as_view(), name='trip_list'),
    # Trip CRUD
    path('trip/new/', views.TripCreateView.as_view(), name='trip_create'),
    path('trip/<int:pk>/', views.TripDetailView.as_view(), name='trip_detail'),
    path('trip/<int:pk>/edit/', views.TripUpdateView.as_view(), name='trip_update'),
    path('trip/<int:pk>/delete/', views.TripDeleteView.as_view(), name='trip_delete'),
]

