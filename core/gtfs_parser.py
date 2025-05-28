"""
Module: GTFSParser

Parses static GTFS data from a zip file, providing access to:
- Stop information (IDs, names, coordinates)
- Routes serving a specific stop
- Agency details

Dependencies:
- csv (for reading GTFS text files)
- zipfile (for accessing compressed GTFS data)

Author: Nwadilioramma Azuka-Onwuka
"""

import csv
import zipfile


class GTFSParser:
    """
    A parser for reading GTFS static data files from a zip archive.
    """

    def __init__(self, zip_path):
        """
        Initialize the parser with the path to the GTFS zip file.
        Args:
            zip_path (str): Path to the GTFS .zip archive.
        """
        self.zip_path = zip_path

    def parse_stops(self):
        """
        Parse stops.txt and return a list of stop details.
        Returns:
            list of dicts: Each containing stop_id, stop_name, latitude, longitude.
        """
        stops = []
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            with zip_ref.open('stops.txt') as file:
                reader = csv.DictReader(file.read().decode('utf-8').splitlines())
                for row in reader:
                    stops.append({
                        'stop_id': row['stop_id'],
                        'stop_name': row['stop_name'],
                        'lat': float(row['stop_lat']),
                        'lon': float(row['stop_lon'])
                    })
        return stops

    def get_routes_for_stop(self, stop_id):
        """
        Get all unique routes that serve a given stop.
        Args:
            stop_id (str): The ID of the stop.
        Returns:
            list of route IDs (sorted).
        """
        routes = set()
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            # Build trip_id → route_id mapping
            trips = csv.DictReader(zip_ref.open('trips.txt').read().decode('utf-8').splitlines())
            trip_to_route = {row['trip_id']: row['route_id'] for row in trips}

            # Identify trips stopping at the specified stop_id
            stop_times = csv.DictReader(zip_ref.open('stop_times.txt').read().decode('utf-8').splitlines())
            for row in stop_times:
                if row['stop_id'] == stop_id:
                    route = trip_to_route.get(row['trip_id'])
                    if route:
                        routes.add(route)
        return sorted(routes)

    def get_agency_info(self):
        """
        Get agency details from agency.txt.
        Returns:
            list of dicts: Each containing agency name, URL, timezone, language, and phone number.
        """
        agencies = []
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            with zip_ref.open('agency.txt') as file:
                reader = csv.DictReader(file.read().decode('utf-8').splitlines())
                for row in reader:
                    agencies.append({
                        'Agency Name': row.get('agency_name'),
                        'Agency URL': row.get('agency_url'),
                        'Timezone': row.get('agency_timezone'),
                        'Agency Language': row.get('agency_lang'),
                        'Agency Phone Number': row.get('agency_phone')
                    })
        return agencies
