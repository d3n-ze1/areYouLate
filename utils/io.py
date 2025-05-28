"""
Module: io

Provides utility functions for:
- Prompting the user to select a route from a list.
- Checking if the user wants to quit the application.

Author: Nwadilioramma Azuka-Onwuka
"""

def prompt_route_selection(routes):
    """
    Display a list of routes and prompt the user to select one.
    Args:
        routes (list): A list of route IDs or names.
    Returns:
        str: The selected route from the list.
    """
    print("Available routes:")
    for i, r in enumerate(routes):
        print(f"[{i}] {r}")
    while True:
        choice = input("Select route number: ").strip()
        if choice.isdigit() and int(choice) in range(len(routes)):
            return routes[int(choice)]
        print("Invalid selection. Please enter a valid number.")

def quit_check(input_text):
    """
    Check if the user entered a quit command and exit if so.
    Args:
        input_text (str): The user input string.
    """
    if input_text.lower() in {"q", "quit"}:
        print("Exiting...")
        exit()
