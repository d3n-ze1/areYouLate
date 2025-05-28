"""
Module: AlertFetcher

Fetches and displays GTFS real-time service alerts using the Google Transit feed.
Allows users to track specific routes, view affected stops, and read detailed alert information.

Dependencies:
- google.transit.gtfs_realtime_pb2
- requests
- config (project configuration)
- utils.time_converter (timestamp formatting)
- geopy (for reverse geocoding stop locations, optional)

Author: Nwadilioramma Azuka-Onwuka
"""

from google.transit import gtfs_realtime_pb2
import requests
import config
from utils.time_converter import convert_timestamp
from geopy.geocoders import Nominatim


class AlertFetcher:
    """
    A class to fetch, parse, and display transit service alerts.
    """

    FEED_URL = config.ALERT_FEED_URL  # URL to the GTFS real-time alert feed

    def __init__(self):
        """
        Initialize AlertFetcher with a geolocator (for optional reverse geocoding).
        """
        self.geolocator = Nominatim(user_agent="transit_locator")

    def reverse_geocode(self, lat, lon):
        """
        Convert latitude and longitude into a human-readable address.
        Used for enriching stop information (optional).
        """
        try:
            location = self.geolocator.reverse((lat, lon), timeout=10)
            return location.address if location else "Unknown location"
        except Exception:
            return "(geocoding failed)"

    def fetch_alerts(self):
        """
        Fetch and parse alerts from the GTFS real-time feed.
        Returns:
            A list of dictionaries containing alert details.
        """
        try:
            response = requests.get(self.FEED_URL)
            response.raise_for_status()
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
        except Exception as e:
            print(f"❌ Error fetching or parsing alerts: {e}")
            return []

        alerts = []
        for entity in feed.entity:
            if entity.HasField("alert"):
                alert = entity.alert
                affected_routes = set()
                stop_locations = set()

                # Collect affected routes and stops
                for informed in alert.informed_entity:
                    if informed.route_id:
                        affected_routes.add(informed.route_id.upper())
                    if informed.stop_id:
                        stop_locations.add(informed.stop_id)

                # Extract header, description, and active periods
                header = "\n".join(t.text for t in alert.header_text.translation)
                description = "\n".join(t.text for t in alert.description_text.translation)
                periods = [(convert_timestamp(p.start), convert_timestamp(p.end)) for p in alert.active_period]

                alerts.append({
                    "header": header,
                    "description": description,
                    "active_periods": periods,
                    "routes": affected_routes,
                    "stops": list(stop_locations)
                })
        return alerts

    def display_alerts(self, tracked_routes=None):
        """
        Provide an interactive menu for users to view and manage transit alerts.
        Args:
            tracked_routes (list or set): Optional list of pre-selected routes to monitor.
        """
        print("""
[Alert Fetcher]
Commands:
  add <ROUTE_ID>      → Track a route (e.g., add 10)
  remove <ROUTE_ID>   → Stop tracking a route
  list                → Show tracked routes
  show                → Display alerts for tracked routes
  all                 → Show all alerts (ignore route filter)
  back                → Return to main menu
""")
        user_routes = set() if tracked_routes is None else set(tracked_routes)

        while True:
            command = input("AlertFetcher >> ").strip().lower()

            if command == "all":
                user_routes = None
                print("Type 'show' to display all alerts, or 'back' to cancel.")

            elif command.startswith("add "):
                route = command[4:].strip().upper()
                if route in user_routes:
                    print(f"{route} is already in your tracked list.")
                else:
                    user_routes.add(route)
                    print(f"{route} added to tracked routes (type 'show' to see alerts).")

            elif command.startswith("remove "):
                route = command[7:].strip().upper()
                if route in user_routes:
                    user_routes.remove(route)
                    print(f"{route} removed from tracked routes.")
                else:
                    print(f"{route} is not in your tracked list.")

            elif command == "show":
                break

            elif command == "list":
                print("Tracked Routes:", ", ".join(user_routes) if user_routes else "(none)")

            elif command == "back":
                print("Returning to main menu.")
                return

            elif command == "help":
                print("""
Commands:
  add <ROUTE_ID>      → Track a route (e.g., add 10)
  remove <ROUTE_ID>   → Stop tracking a route
  list                → Show tracked routes
  show                → Display alerts for tracked routes
  all                 → Show all alerts (ignore route filter)
  back                → Return to main menu
""")
            else:
                print("Invalid command. Type 'help' for available options.")

        # Fetch and display alerts based on user selection
        alerts = self.fetch_alerts()
        if not alerts:
            print("✅ No current alerts.")
            return

        found = False
        for alert in alerts:
            if user_routes is None or alert["routes"] & set(r.upper() for r in user_routes):
                found = True
                print("----- ALERT -----")
                print("Header:", alert["header"])
                print("Description:", alert["description"])
                for start, end in alert["active_periods"]:
                    print("Start:", start)
                    print("End:  ", end)
                if alert["routes"]:
                    print("Routes affected:", ", ".join(alert["routes"]))
                if alert["stops"]:
                    print("Stops affected:")
                    for stop_id in alert["stops"]:
                        print(f"  - Stop ID: {stop_id}")
                print()

        if not found:
            print("✅ No alerts affecting your selected routes.")
