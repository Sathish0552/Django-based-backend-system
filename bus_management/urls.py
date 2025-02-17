from django.contrib import admin
from django.urls import path, include
from buses.views import home  # Import homepage view

urlpatterns = [
    path('', home, name='home'),  # Homepage (index.html)
    path('admin/', admin.site.urls),  # Django Admin Panel
    path('', include('buses.urls')),  # Includes buses' UI and API routes
]
