from django.contrib import admin

from .models import Destination, DestinationDistance, DestinationImage, Trip


class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1
    fields = ('image', 'caption', 'is_primary', 'sort_order')


class DestinationInline(admin.StackedInline):
    model = Destination
    extra = 0
    fields = ('name', 'address', 'latitude', 'longitude', 'sort_order')
    show_change_link = True


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination_count', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DestinationInline]

    @admin.display(description='Destinations')
    def destination_count(self, obj):
        return obj.destinations.count()


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'trip', 'address', 'latitude', 'longitude', 'sort_order', 'created_at')
    list_filter = ('trip',)
    list_select_related = ('trip',)
    date_hierarchy = 'created_at'
    search_fields = ('name', 'description', 'address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DestinationImageInline]


@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'destination', 'is_primary', 'sort_order')
    list_filter = ('is_primary',)
    list_select_related = ('destination__trip',)
    search_fields = ('caption', 'destination__name')

    @admin.display(description='Image')
    def image_name(self, obj):
        return str(obj)


@admin.register(DestinationDistance)
class DestinationDistanceAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'haversine_distance_km',
        'driving_distance_km',
        'driving_duration_minutes',
    )
    list_filter = ('from_destination__trip',)
    list_select_related = ('from_destination__trip', 'to_destination')
    search_fields = ('from_destination__name', 'to_destination__name')
