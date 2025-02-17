from django.urls import path
from .views import list_buses,track_bus_location_page,get_bus_location,logout_view,register_bus, get_bus_details, submit_bus_location, get_bus_stats,filter_buses

urlpatterns = [
    # List of buses
    path('buses/', list_buses, name='list-buses'),
    
    # Register a new bus
    path('buses/register/', register_bus, name='register-bus'),
    
    # Bus details page
    path('buses/<int:pk>/', get_bus_details, name='bus-details'),
    
    # Submit bus location
    path('buses/location/', submit_bus_location, name='submit-bus-location'),
    
    
    
    
    
    # New API endpoint to get bus statistics
    path('api/bus/stats/', get_bus_stats, name='bus-stats'),
    path('api/buses/filter-buses/', filter_buses, name='filter_buses'),
    path('logout/', logout_view, name='logout'),
    path('track-bus-location/', track_bus_location_page, name='track_bus_location_page'),
    
    # The API endpoint that returns the bus location based on name and route number
    path('api/bus/location', get_bus_location, name='get_bus_location'),
]
