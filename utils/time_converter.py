"""
Module: time_converter

Provides a utility function to convert Unix timestamps into human-readable date and time strings.

Author: Nwadilioramma Azuka-Onwuka
"""

import datetime

def convert_timestamp(timestamp):
    """
    Convert a Unix timestamp (in seconds) to a formatted date-time string.
    Args:
        timestamp (int or float): The Unix timestamp to convert.
    Returns:
        str: The formatted date-time string (e.g., '2024-05-27 08:15:30 PM').
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %I:%M:%S %p')
