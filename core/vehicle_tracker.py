"""
Module: VehicleTracker

Provides real-time tracking of transit vehicles using GTFS real-time VehiclePosition feed.
Allows users to interactively select routes to track and view live vehicle locations.

Dependencies:
- config (project configuration)
- requests
- geopy (for reverse geocoding)
- google.transit.gtfs_realtime_pb2 (protobuf decoding)
- utils.time_converter (timestamp formatting)

Author: Nwadilioramma Azuka-Onwuka
"""

import config
import requests
from geopy.geocoders import Nominatim
from google.transit import gtfs_realtime_pb2
from utils.time_converter import convert_timestamp


class VehicleTracker:
    """
    A class to interactively track real-time vehicle locations for selected transit routes.
    """

    FEED_URL = config.VEHICLE_FEED_URL  # GTFS real-time VehiclePositions feed URL

    def __init__(self):
        """
        Initialize the tracker with an empty route list and a geolocator.
        """
        self.routes = []  # List of routes currently being tracked
        self.geolocator = Nominatim(user_agent="halifax_transit_vehicle_locator")

    def reverse_geocode(self, lat, lon):
        """
        Convert latitude and longitude into a human-readable address.
        Args:
            lat (float): Latitude.
            lon (float): Longitude.
        Returns:
            str: Resolved address or fallback string.
        """
        try:
            location = self.geolocator.reverse((lat, lon), timeout=10)
            return location.address if location else "Unknown location"
        except Exception:
            return "(geocoding failed)"

    def interactive_track(self):
        """
        Launch an interactive command loop for managing tracked routes and showing vehicle updates.
        """
        print("""
[Vehicle Tracker]
Commands:
  add <ROUTE>      → Add a route to track (e.g., add 10)
  remove <ROUTE>   → Stop tracking a route
  routes           → Show all currently tracked routes
  show             → Display real-time info for tracked buses
  help             → Show this help message again
  back             → Return to the main menu
""")
        while True:
            print("\n[Vehicle Tracker] Options: add <ROUTE>, remove <ROUTE>, show, routes, help, back")
            user_input = input("Enter command >> ").strip().lower()

            if user_input == "back":
                break
            elif user_input.startswith("add "):
                route = user_input[4:].upper()
                if route not in self.routes:
                    self.routes.append(route)
                    print(f"Added route {route}.")
                else:
                    print(f"{route} is already being tracked.")
            elif user_input.startswith("remove "):
                route = user_input[7:].upper()
                if route in self.routes:
                    self.routes.remove(route)
                    print(f"Removed route {route}.")
                else:
                    print(f"{route} is not being tracked.")
            elif user_input == "routes":
                print("Tracking:", ", ".join(self.routes) or "None")
            elif user_input == "show":
                self.fetch()
            elif user_input == "help":
                print("""
[Vehicle Tracker Help]
Commands:
  add <ROUTE>      → Add a route to track (e.g., add 10)
  remove <ROUTE>   → Stop tracking a route
  routes           → Show all currently tracked routes
  show             → Display real-time info for tracked buses
  help             → Show this help message again
  back             → Return to the main menu
""")
            else:
                print("Invalid command. Type 'help' to see available options.")

    def fetch(self):
        """
        Fetch and display real-time vehicle updates for the tracked routes.
        """
        try:
            response = requests.get(self.FEED_URL)
            response.raise_for_status()
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
        except Exception as e:
            print(f"Error fetching vehicle data: {e}")
            return

        found = False
        for entity in feed.entity:
            if entity.HasField("vehicle"):
                v = entity.vehicle
                if v.trip.route_id in self.routes:
                    found = True
                    print(f"\n--- Vehicle Update ---")
                    lat = v.position.latitude
                    lon = v.position.longitude
                    place = self.reverse_geocode(lat, lon)
                    print(f"Route: {v.trip.route_id}")
                    print(f"Location: {place} (Lat: {lat:.4f}, Lon: {lon:.4f})")
                    print(f"Timestamp: {convert_timestamp(v.timestamp)}")

        if not found:
            print("No vehicles found on the tracked routes.")
