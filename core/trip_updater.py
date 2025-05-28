"""
Module: TripUpdater

Fetches and displays GTFS real-time trip updates for specific stops and routes.
Allows interactive commands to check upcoming bus arrivals, search stops,
and explore routes at a stop.

Dependencies:
- google.transit.gtfs_realtime_pb2
- requests
- geopy (reverse geocoding)
- core.gtfs_parser (for static route/stop lookups)
- utils.stop_finder (for interactive stop finding)
- utils.time_converter (timestamp conversion)

Author: Nwadilioramma Azuka-Onwuka
"""

from google.transit import gtfs_realtime_pb2
import requests
import config
from utils.stop_finder import StopFinder
from utils.time_converter import convert_timestamp
from geopy.geocoders import Nominatim
from core.gtfs_parser import GTFSParser  # Needed for route lookup


class TripUpdater:
    """
    Provides interactive tools to fetch and display real-time arrivals
    at transit stops using the GTFS real-time TripUpdate feed.
    """

    FEED_URL = config.TRIPS_FEED_URL  # URL to the live trip updates feed

    def __init__(self):
        """
        Initialize the TripUpdater with a geolocator for reverse geocoding.
        """
        self.geolocator = Nominatim(user_agent="halifax_transit_trip_updater")

    def reverse_geocode(self, lat, lon):
        """
        Convert latitude and longitude to a human-readable address.
        Args:
            lat (float): Latitude
            lon (float): Longitude
        Returns:
            str: Address or fallback text.
        """
        try:
            location = self.geolocator.reverse((lat, lon), timeout=10)
            return location.address if location else "Unknown location"
        except Exception:
            return "(geocoding failed)"

    def interactive_arrivals(self):
        """
        Launch an interactive command menu to check arrivals and explore stops/routes.
        """
        print("""
[Trip Updater]
Commands:
  find               → Find stops
  stop <STOP_ID>     → Set the stop ID for updates (must be 4-digit)
  route <ROUTE_ID>   → Show arrivals for a specific route
  routes             → Show all routes serving the stop
  all                → Show all arrivals at a stop
  clear              → Clear the currently set stop ID
  help               → Show this help message again
  back               → Return to the main menu
""")
        stop_id = ""  # Currently selected stop ID

        while True:
            command = input("TripUpdater >> ").strip().lower()

            if command.startswith("stop "):
                # Set the stop ID (must be a 4-digit number)
                candidate = command[5:].strip()
                if candidate.isdigit() and len(candidate) == 4:
                    stop_id = candidate
                    print(f"Stop set to {stop_id}.")
                else:
                    print("Invalid stop ID. Must be a 4-digit number.\n")

            elif command.startswith("route "):
                # Show arrivals for a specific route at the current stop
                if not stop_id:
                    print("Please enter a stop ID first (use: stop <STOP_ID>)\n")
                else:
                    route_id = command[6:].strip()
                    self.get_arrivals(stop_id, route_id)

            elif command == "routes":
                # List all routes serving the current stop
                if not stop_id:
                    print("Please enter a stop ID first (use: stop <STOP_ID>)\n")
                else:
                    parser = GTFSParser("Static_data.zip")
                    available_routes = parser.get_routes_for_stop(stop_id)
                    if available_routes:
                        print("Routes at stop:", ", ".join(available_routes))
                    else:
                        print("No routes found for that stop.\n")

            elif command == "all":
                # Show all arrivals at the current stop (ignore route filtering)
                if not stop_id:
                    print("Please enter a stop ID first (use: stop <STOP_ID>)\n")
                else:
                    self.get_arrivals(stop_id, "all")

            elif command == "clear":
                stop_id = ""
                print("Cleared stop ID. Use 'stop <STOP_ID>' to set a new one.\n")

            elif command == "back":
                print("Returning to main menu.\n")
                break

            elif command == "find":
                # Launch the StopFinder interactive menu
                self.stop_finder_menu()

            elif command == "help":
                # Show the help menu again
                print("""
[Trip Updater Help]
Commands:
  find               → Find stops
  stop <STOP_ID>     → Set the stop ID for updates (must be 4-digit)
  route <ROUTE_ID>   → Show arrivals for a specific route
  routes             → Show all routes serving the stop
  all                → Show all arrivals at a stop
  clear              → Clear the currently set stop ID
  help               → Show this help message again
  back               → Return to the main menu
""")
            else:
                print("Invalid command. Type 'help' for options.\n")

    def get_arrivals(self, stop_id, route_id):
        """
        Fetch and display upcoming arrivals for a stop and route.
        Args:
            stop_id (str): Stop ID to check.
            route_id (str): Route ID or 'all' to show all.
        """
        try:
            response = requests.get(self.FEED_URL)
            response.raise_for_status()
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
        except Exception as e:
            print(f"❌ Error fetching trip updates: {e}")
            return

        trips = []
        for entity in feed.entity:
            if entity.HasField("trip_update"):
                trip = entity.trip_update
                if route_id == "all" or trip.trip.route_id.upper() == route_id.upper():
                    for stu in trip.stop_time_update:
                        if stu.stop_id == stop_id:
                            trips.append({
                                "route_id": trip.trip.route_id,
                                "stop_sequence": stu.stop_sequence,
                                "arrival_time": stu.arrival.time,
                                "departure_time": stu.departure.time
                            })

        trips.sort(key=lambda x: x["arrival_time"])

        if not trips:
            print("No upcoming arrivals for that stop and route.\n")
            return

        for trip in trips:
            # TODO: Replace with actual stop lat/lon if available
            # place = self.reverse_geocode(lat, lon)
            print(f"→ Route {trip['route_id']} @ Stop {stop_id}")
            print(f"   Stop Seq: {trip['stop_sequence']}")
            print(f"   Arrival: {convert_timestamp(trip['arrival_time'])}")
            print(f"   Departure: {convert_timestamp(trip['departure_time'])}")
            print("-" * 30)

    def stop_finder_menu(self):
        """
        Launch the StopFinder interactive menu for searching stops.
        """
        stop_finder = StopFinder()
        while True:
            print("""
[Stop Finder]
1 - Search for a stop by name
2 - Find 3 closest stops by coordinates
3 - Get all stops served by a route
B - Back to previous menu
""")
            option = input("StopFinder >> ").strip().lower()
            if option == "1":
                keyword = input("Enter part of the stop name: ").strip()
                stop_finder.find_stops_by_name(keyword)
            elif option == "2":
                try:
                    lat = float(input("Enter latitude: ").strip())
                    lon = float(input("Enter longitude: ").strip())
                    stop_finder.find_closest_stops(lat, lon)
                except ValueError:
                    print("Invalid coordinates.")
            elif option == "3":
                route_id = input("Enter Route ID: ").strip().upper()
                stop_finder.find_stops_for_route(route_id)
            elif option == "b":
                break
            else:
                print("Invalid option. Choose 1, 2, 3, or B.")
