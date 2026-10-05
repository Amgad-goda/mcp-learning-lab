# server.py
from typing import Any, Dict, List
from fastmcp import FastMCP
from db import (
    save_flight,
    list_saved_flights,
    update_saved_flight,
    delete_saved_flight,
    drop_collection,
)
from flights import search_flights

# Initialize the FastMCP server instance
mcp = FastMCP("Flight Deals & Tracker Server")


@mcp.tool()
def find_flights(origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
    """
    Search for available flights between two airports on a specific date.

    Args:
        origin (str): Departure airport 3-letter IATA code (e.g., 'JFK').
        destination (str): Arrival airport 3-letter IATA code (e.g., 'LHR').
        date (str): Travel date strictly formatted as 'YYYY-MM-DD'.

    Returns:
        List[Dict[str, Any]]: A list of flight options sorted by cheapest price first.
    """
    return search_flights(origin=origin, destination=destination, date=date)


@mcp.tool()
def save_flight_to_db(
    airline: str,
    price: float,
    origin: str,
    destination: str,
    date: str,
    duration_minutes: int = 0,
    stops: int = 0,
) -> str:
    """
    Save an exact flight record to MongoDB Atlas for tracking.
    All details must come directly from the find_flights tool output.

    Args:
        airline (str): Name of the airline (e.g., 'Icelandair').
        price (float): Flight price as a numeric value.
        origin (str): Departure airport code (e.g., 'JFK').
        destination (str): Arrival airport code (e.g., 'LHR').
        date (str): Date of travel formatted as 'YYYY-MM-DD'.
        duration_minutes (int): Total flight duration in minutes. Defaults to 0.
        stops (int): Number of flight stops/layovers. Defaults to 0.

    Returns:
        str: The inserted document's MongoDB ObjectId string.
    """
    flight_data = {
        "airline": airline,
        "price": price,
        "origin": origin,
        "destination": destination,
        "date": date,
        "duration_minutes": duration_minutes,
        "stops": stops,
    }
    return save_flight(flight_data)


@mcp.tool()
def get_saved_flights(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Retrieve tracked flights from MongoDB Atlas.

    Args:
        limit (int): Maximum number of flights to return. Defaults to 10.

    Returns:
        List[Dict[str, Any]]: List of tracked flight documents with stringified _id fields.
    """
    return list_saved_flights(limit=limit)


@mcp.tool()
def update_flight_record(flight_id: str, updates: Dict[str, Any]) -> str:
    """
    Update fields of an existing tracked flight by its MongoDB ObjectId.

    Args:
        flight_id (str): The 24-character hexadecimal ObjectId of the document.
        updates (Dict[str, Any]): Dictionary of key-value pairs to update.

    Returns:
        str: Status message indicating success or failure.
    """
    success = update_saved_flight(flight_id, updates)
    if success:
        return f"Flight {flight_id} updated successfully."
    return f"Failed to update: Flight {flight_id} not found."


@mcp.tool()
def remove_flight_record(flight_id: str, confirm: bool = False) -> str:
    """
    Permanently delete a tracked flight record by its MongoDB ObjectId.

    Args:
        flight_id (str): The 24-character hexadecimal ObjectId to remove.
        confirm (bool): Safety confirmation flag. Must be set to True.

    Returns:
        str: Confirmation or cancellation message.
    """
    return delete_saved_flight(flight_id=flight_id, confirm=confirm)


@mcp.tool()
def purge_all_saved_flights(confirm: bool = False) -> str:
    """
    Drop the entire saved_flights collection from the database.

    Args:
        confirm (bool): Safety confirmation flag. Must be set to True.

    Returns:
        str: Result status message.
    """
    return drop_collection(confirm=confirm)


if __name__ == "__main__":
    mcp.run()