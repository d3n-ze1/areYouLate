"""
Module: StopFinder

Provides tools to:
- Search transit stops by name.
- Find the closest stops to a given coordinate.
- List all stops served by a specific route.

Uses GTFS static data loaded from a .zip file.

Dependencies:
- zipfile (for reading compressed GTFS files)
- csv (for parsing GTFS text files)
- math (for haversine distance calculations)
- core.gtfs_parser (to parse stops list)

Author: Nwadilioramma Azuka-Onwuka
"""

import zipfile
import csv
from math import radians, sin, cos, sqrt, atan2
from core.gtfs_parser import GTFSParser


class StopFinder:
    """
    A class for searching and analyzing GTFS stops.
    """

    def __init__(self, zip_path="data/Static_data.zip"):
        """
        Initialize StopFinder.
        Args:
            zip_path (str): Path to the GTFS static zip file.
        """
        self.zip_path = zip_path
        self.parser = GTFSParser(zip_path)

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great-circle distance between two points on Earth.
        Args:
            lat1, lon1 (float): Latitude and longitude of point 1.
            lat2, lon2 (float): Latitude and longitude of point 2.
        Returns:
            float: Distance in kilometers.
        """
        R = 6371  # Earth radius in km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def find_stops_by_name(self, keyword):
        """
        Search stops whose names contain the given keyword.
        Args:
            keyword (str): Part or full name of the stop (case-insensitive).
        Returns:
            list of dicts: Matching stops.
        """
        matches = [s for s in self.parser.parse_stops() if keyword.lower() in s['stop_name'].lower()]
        if matches:
            for stop in matches:
                print(f"{stop['stop_id']} → {stop['stop_name']}")
        else:
            print("No stops found.")
        return matches

    def find_closest_stops(self, lat, lon, count=3):
        """
        Find the N closest stops to a given latitude and longitude.
        Args:
            lat (float): Latitude.
            lon (float): Longitude.
            count (int): Number of closest stops to return (default 3).
        Returns:
            list of (stop dict, distance) tuples.
        """
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            print("Invalid latitude or longitude.")
            return []

        stops = self.parser.parse_stops()
        distances = [(s, self.haversine(lat, lon, s['lat'], s['lon'])) for s in stops]
        closest = sorted(distances, key=lambda x: x[1])[:count]

        for stop, dist in closest:
            print(f"{stop['stop_id']} → {stop['stop_name']} ({dist:.2f} km)")
        return closest

    def find_stops_for_route(self, route_id):
        """
        Find all stops served by a specific route.
        Args:
            route_id (str): Route ID to search.
        Returns:
            list of stop dicts.
        """
        stop_ids = set()

        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            # Build set of trip IDs associated with the route
            trips = csv.DictReader(zip_ref.open('trips.txt').read().decode('utf-8').splitlines())
            trip_ids = {row['trip_id'] for row in trips if row['route_id'].upper() == route_id.upper()}

            # Collect all stop IDs from the selected trips
            stop_times = csv.DictReader(zip_ref.open('stop_times.txt').read().decode('utf-8').splitlines())
            for row in stop_times:
                if row['trip_id'] in trip_ids:
                    stop_ids.add(row['stop_id'])

        # Filter the stop list to only those in stop_ids
        stops = [s for s in self.parser.parse_stops() if s['stop_id'] in stop_ids]
        if stops:
            for stop in stops:
                print(f"{stop['stop_id']} → {stop['stop_name']}")
        else:
            print("No stops found for that route.")
        return stops
