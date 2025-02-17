from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
import random
from django.http import JsonResponse
from .models import Bus, BusLocation
from .serializers import BusSerializer, BusLocationSerializer
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from geopy.geocoders import Nominatim

# 📌 Home View (Loads HTML template)
def home(request):
    return render(request, 'home.html')  

def logout_view(request):
    logout(request)  # Logs the user out
    return render(request, 'home.html') 

def get_bus_stats(request):
    total_buses = Bus.objects.count()
    active_buses = Bus.objects.filter(status='active').count()
    inactive_buses = Bus.objects.filter(status='inactive').count()
    maintenance_buses = Bus.objects.filter(status='maintenance').count()
    
    # Get the latest bus location
    latest_location = BusLocation.objects.order_by('-timestamp').first()
    latest_location_data = {
        'latitude': latest_location.latitude if latest_location else None,
        'longitude': latest_location.longitude if latest_location else None,
    }
    
    stats_data = {
        'total_buses': total_buses,
        'active_buses': active_buses,
        'inactive_buses': inactive_buses,
        'maintenance_buses': maintenance_buses,
        'latest_location': latest_location_data,
    }
    
    return JsonResponse(stats_data)

def track_bus_location_page(request):
    return render(request, 'track_bus_locations.html')

def get_bus_location(request):
    bus_name = request.GET.get('name')
    route_number = request.GET.get('route_number')

    if not bus_name or not route_number:
        return JsonResponse({'error': 'Bus name and route number are required'}, status=400)

    try:
        # Get the bus and its latest location
        bus = Bus.objects.get(name=bus_name, route_number=route_number)
        latest_location = bus.locations.latest('timestamp')  # Get the most recent location

        # Use Geopy's Nominatim to reverse geocode latitude and longitude
        geolocator = Nominatim(user_agent="bus_tracker")
        location = geolocator.reverse((latest_location.latitude, latest_location.longitude), language="en")

        # If location is found, return it
        place = location.address if location else "Location Unknown"

        return JsonResponse({
            'name': bus.name,
            'route_number': bus.route_number,
            'status': bus.status,
            'latitude': latest_location.latitude,
            'longitude': latest_location.longitude,
            'place': place
        })
    
    except Bus.DoesNotExist:
        return JsonResponse({'error': 'Bus not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




def filter_buses(request):
    if request.method == "GET":
        # Get search term and filter from the query parameters
        search_term = request.GET.get('search', '').strip().lower()
        status = request.GET.get('status', '').strip().lower()

        # Start filtering buses
        buses = Bus.objects.all()

        if search_term:
            buses = buses.filter(
                name__icontains=search_term  # Search by name
            )   # Search by route number

        if status:
            buses = buses.filter(status=status)  # Filter by status

        # Check if any buses are found
        bus_found = buses.exists()

        # Prepare response message based on availability
        if bus_found:
            message = f"Bus '{search_term}' is available!"
        else:
            message = f"Bus '{search_term}' is not available."

        # Return availability status as JSON response
        return JsonResponse({'message': message, 'available': bus_found})

    return JsonResponse({'error': 'Invalid method'}, status=405)


# 📌 List Buses (API + HTML)
@api_view(['GET'])
def list_buses(request):
    if request.headers.get('Accept') == 'application/json':  # API request
        cache_key = "bus_list"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            buses = Bus.objects.all()
            serializer = BusSerializer(buses, many=True)
            bus_data = serializer.data
            cache.set(cache_key, bus_data, timeout=300)
        else:
            bus_data = cached_data

        return Response(bus_data, status=status.HTTP_200_OK)
    
    # Render HTML Template for UI
    buses = Bus.objects.all()
    return render(request, 'buses_list.html', {'buses': buses})




@api_view(['GET', 'POST'])
def register_bus(request):
    if request.method == 'GET':
        # Serve the registration form (e.g., return the HTML page)
        return render(request, 'register_bus.html')

    if request.method == 'POST':
        # Check for bus name duplication (case-insensitive)
        bus_name = request.data.get('name')
        if Bus.objects.filter(name__iexact=bus_name).exists():
            return JsonResponse({
                'success': False,
                'message': 'This bus name already exists. Please try a new bus name.'
            }, status=400)

        # Proceed with registration (no duplicate route number check)
        serializer = BusSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'success': True,
                'message': 'Bus registered successfully!'
            })
        else:
            # Log the validation errors for debugging
            logger.error(f"Validation errors: {serializer.errors}")

            # Return the validation errors in the response
            return JsonResponse({
                'success': False,
                'message': 'There was an issue with the bus registration. Please check the details and try again.',
                'errors': serializer.errors
            }, status=400)



# Get Bus Details (API + HTML)
@api_view(['GET'])
def get_bus_details(request, pk):
    bus = get_object_or_404(Bus, pk=pk)

    # Check if the request is an API request (JSON response)
    if request.headers.get('Accept') == 'application/json':  
        serializer = BusSerializer(bus)
        # Return bus data in JSON format without latitude, longitude, and place
        return Response({
            'id': bus.id,
            'name': bus.name,
            'route_number': bus.route_number,
            'status': bus.status,
        }, status=status.HTTP_200_OK)

    # Render the UI template for bus details (HTML page)
    return render(request, 'bus_details.html', {
        'bus': bus,
    })



# 📌 Submit Bus Location (API + HTML Form)
@api_view(['GET', 'POST'])
# Your view for submitting bus location
def submit_bus_location(request):
    if request.method == 'POST':
        bus_id = request.POST['bus']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        
        # Find the bus by ID (assuming the Bus model has a unique ID)
        bus = Bus.objects.get(id=bus_id)
        
        # Update the bus location
        bus.latitude = latitude
        bus.longitude = longitude
        bus.save()

        # Add a success message
        messages.success(request, "Bus location submitted successfully!")

        # Stay on the same page with the success message displayed
        return render(request, 'submit_location.html')

    return render(request, 'submit_location.html')


    


# 📌 Retrieve Bus Locations (API + HTML)
@api_view(['GET'])
def get_bus_locations(request, bus_id):
    if request.headers.get('Accept') == 'application/json':  # API request
        cache_key = f"bus_location_{bus_id}"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            locations = BusLocation.objects.filter(bus_id=bus_id).order_by('-timestamp')
            serializer = BusLocationSerializer(locations, many=True)
            location_data = serializer.data
            cache.set(cache_key, location_data, timeout=60)
        else:
            location_data = cached_data

        return Response(location_data, status=status.HTTP_200_OK)

    # Render HTML Template
    locations = BusLocation.objects.filter(bus_id=bus_id).order_by('-timestamp')
    return render(request, 'bus_tracking.html', {'locations': locations})


