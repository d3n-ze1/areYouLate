"""
Function: manage_routes

Provides an interactive loop for adding, removing, listing,
and managing the user's tracked bus routes.

Author: Nwadilioramma Azuka-Onwuka
"""

def manage_routes(tracked_routes):
    """
    Interactive route manager.
    Allows the user to add, remove, or list tracked bus routes.
    Args:
        tracked_routes (list): A list of currently tracked route IDs.
    """
    print("""
ROUTE MANAGER COMMANDS:
  add <ROUTE>    → Add a bus route to your tracking list (e.g., add 10)
  remove <ROUTE> → Remove a bus route from your tracking list
  list           → View all tracked routes
  help           → Show this help menu
  back           → Return to main menu
""")

    while True:
        print("\nRoute Manager — Type: add <ROUTE>, remove <ROUTE>, list, back")
        command = input("Command: ").strip().lower()

        if command == "back":
            # Exit the route manager loop
            break

        elif command.startswith("add "):
            # Add a route to the tracking list
            route = command[4:].strip().upper()
            if route in tracked_routes:
                print(f"{route} is already tracked.")
            else:
                tracked_routes.append(route)
                print(f"Tracking {route}.")

        elif command.startswith("remove "):
            # Remove a route from the tracking list
            route = command[7:].strip().upper()
            if route in tracked_routes:
                tracked_routes.remove(route)
                print(f"Stopped tracking {route}.")
            else:
                print(f"{route} is not being tracked.")

        elif command == "list":
            # Display all currently tracked routes
            print("Currently tracking:", ", ".join(tracked_routes) or "None")

        elif command == "help":
            # Show help menu
            print("""
ROUTE MANAGER COMMANDS:
  add <ROUTE>    → Add a bus route to your tracking list (e.g., add 10)
  remove <ROUTE> → Remove a bus route from your tracking list
  list           → View all tracked routes
  help           → Show this help menu
  back           → Return to main menu
""")

        else:
            print("Invalid command. Type 'help' to see available commands.")
