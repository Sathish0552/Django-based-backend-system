from django.contrib import admin
from .models import Bus, BusLocation

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'route_number', 'status')
    search_fields = ('name', 'route_number', 'status')
    list_filter = ('status',)

    # Allow delete permission explicitly
    def has_delete_permission(self, request, obj=None):
        return True  # This ensures the delete option is available

@admin.register(BusLocation)
class BusLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'bus', 'latitude', 'longitude', 'timestamp')
    list_filter = ('bus', 'timestamp')
    search_fields = ('bus__name', 'latitude', 'longitude')
