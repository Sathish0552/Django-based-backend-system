# Bus Management System

## Overview
This is a **Django-based Bus Management System** developed to manage bus data. It includes functionalities like **bus registration**, **location tracking**, and **bus status updates**. The system uses **Django Rest Framework (DRF)** to expose API endpoints for performing these tasks. The system is also optimized with **caching** to improve performance for frequently accessed data.

## Features
- **Bus Registration**: Register buses by providing details such as name, route number, and status.
- **Bus Location Tracking**: Submit and retrieve real-time bus location data (latitude, longitude, timestamp).
- **Caching**: Cache bus list and location data to optimize performance.
- **API Endpoints**: 
  - Register a bus
  - List all buses
  - Retrieve bus details by ID
  - Submit and retrieve bus locations
- **Error Handling**: Handle missing or invalid data, such as bus or location not found.
- **Django Admin Interface**: Manage buses and their locations through the Django admin interface.

## Project Structure
The project consists of the following core components:

- **Bus Model**: Stores bus details such as name, route number, and status.
- **BusLocation Model**: Stores the GPS coordinates and timestamp of bus locations.
- **API Endpoints**: Exposed using Django Rest Framework (DRF) for bus registration, listing, and location tracking.
- **Caching**: Used to improve performance by reducing database hits for bus and location data.

## Installation and Setup

### 1. Clone the Repository:
Clone the project to your local machine using the following command:

git clone https://github.com/Sathish0552/Django-based-backend-system.git

## 2. Navigate to the Project Directory:
Change to the project folder:

cd bus-management-system

## 3. Set Up a Virtual Environment:
It is recommended to use a virtual environment to manage dependencies.



## 4. Install Dependencies:
Install the required dependencies:

## 5. Apply Database Migrations:
Run database migrations to set up the models:

python manage.py migrate

## 6. Run the Development Server:
Start the Django development server:

python manage.py runserver

The application will be available at http://127.0.0.1:8000/.

## API Endpoints
The following API endpoints are available in the system:

## Bus API Endpoints:
POST /api/buses/: Register a new bus with details like name, route number, and status.
GET /api/buses/: List all buses.
GET /api/buses/{id}/: Retrieve details of a specific bus by its ID.

## Bus Location API Endpoints:
POST /api/bus-locations/: Submit a bus location (latitude, longitude, timestamp).
GET /api/bus-locations/{bus_id}/: Retrieve the location history of a bus by its ID.

## Caching
To improve performance, caching is implemented for bus list and location data. This reduces the number of database queries, speeding up the system for frequently accessed information.

## Admin Interface
The Django admin interface is set up to manage bus records and their locations. To access the admin interface:

## Create a superuser account:

python manage.py createsuperuser

Log in to the admin interface at http://127.0.0.1:8000/admin with your superuser credentials.

You can then manage the buses and their locations from the admin panel.

## Error Handling
The system is designed to handle errors gracefully:

If a bus is not found, the API will return a 404 error with an appropriate message.
If the bus location data is incomplete or invalid, the system will respond with a 400 error and prompt for valid data.
