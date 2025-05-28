"""
Main Module: Halifax Transit Assistant

This is the entry point for the Halifax Transit Assistant app.
It provides an interactive console interface to:
- View service alerts
- Track real-time buses
- Check upcoming arrivals by stop and route
- Manage a list of tracked routes
- View agency information

Author: Nwadilioramma Azuka-Onwuka
"""

from core.gtfs_parser import GTFSParser
from core.trip_updater import TripUpdater
from core.alert_fetcher import AlertFetcher
from core.vehicle_tracker import VehicleTracker
from utils.route_manager import manage_routes
from utils.io import prompt_route_selection, quit_check


def main():
    """
    Main menu loop for the Halifax Transit Assistant.
    Initializes key modules and handles user command input.
    """
    print("""
Welcome to the Halifax Transit Assistant!
This tool allows you to:
- View current service alerts affecting Halifax Transit
- Track buses on selected routes
- Get upcoming arrival times for stops
- Manage your list of routes of interest
""")

    def show_help():
        """
        Display help menu options.
        """
        print("""
MAIN MENU OPTIONS:
1 - View Service Alerts
2 - Track a Bus: Add/remove/view routes to track real-time vehicles
3 - Get Route Updates: Interactive tool for tracking by stop & route
4 - Manage Tracked Routes: Add/remove routes from your tracked list
5 - Agency Info
H - Help
Q - Quit the application
""")

    # Setup GTFS data parser and core modules
    gtfs_path = "data/Static_data.zip"
    parser = GTFSParser(gtfs_path)
    alert_fetcher = AlertFetcher()
    trip_updater = TripUpdater()
    vehicle_tracker = VehicleTracker()
    tracked_routes = []  # User’s currently tracked routes

    while True:
        # Main menu prompt
        print("""
=== Halifax Transit Assistant ===
1. View Service Alerts
2. Track a Bus
3. Get Route Updates (Arrivals)
4. Manage Tracked Routes
5. Agency Info
H. Help
Q. Quit
""")
        choice = input("Select an option: ").strip().lower()
        quit_check(choice)  # Check for quit command

        if choice == "1":
            print("You can choose which routes to see alerts for, or type 'all' to see everything.\n")
            alert_fetcher.display_alerts(tracked_routes)

        elif choice == "2":
            print("You can track buses by route and view live vehicle positions.")
            vehicle_tracker.routes = tracked_routes
            vehicle_tracker.interactive_track()

        elif choice == "3":
            print("You can interactively check bus arrivals by stop ID and route.\n")
            trip_updater.interactive_arrivals()

        elif choice == "4":
            manage_routes(tracked_routes)

        elif choice == "5":
            # Display agency information from GTFS static data
            agencies = parser.get_agency_info()
            if agencies:
                first_agency = agencies[0]
                print("\n=== Agency Information ===")
                for key, value in first_agency.items():
                    print(f"{key}: {value}")
            else:
                print("No agency info found.")

        elif choice == "h":
            show_help()

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
