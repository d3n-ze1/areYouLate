"""
Module: config

Stores GTFS real-time feed URLs used by the application.

IMPORTANT:
If you switch to a different city or transit provider,
you must replace these URLs with that provider’s official GTFS real-time feeds.

Author: Nwadilioramma Azuka-Onwuka
"""

# Halifax Transit GTFS real-time alerts feed (e.g., service disruptions, detours)
ALERT_FEED_URL = "http://gtfs.halifax.ca/realtime/Alert/Alerts.pb"

# Halifax Transit GTFS real-time trip updates feed (e.g., arrival/departure predictions)
TRIPS_FEED_URL = "http://gtfs.halifax.ca/realtime/TripUpdate/TripUpdates.pb"

# Halifax Transit GTFS real-time vehicle positions feed (e.g., live bus locations)
VEHICLE_FEED_URL = "http://gtfs.halifax.ca/realtime/Vehicle/VehiclePositions.pb"

# ⚠️ TO UPDATE:
# Visit your target city’s open data or transit API portal and replace the above URLs
# with the correct feed links provided for that region.
