# flights.py
from datetime import datetime
import re
from typing import Any, Dict, List
from fast_flights import FlightQuery, Passengers, create_filter, get_flights


def _clean_price(price_val: Any) -> float:
    """Helper to convert raw price objects or currency strings into a clean float."""
    if isinstance(price_val, (int, float)):
        return float(price_val)
    if not price_val or str(price_val).strip() in ("N/A", "None", ""):
        return 0.0
    
    # Extract only digits and decimal points (removes $, €, commas, etc.)
    cleaned = re.sub(r"[^\d.]", "", str(price_val))
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def search_flights(origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
    """
    Searches one-way flights using fast-flights.
    Date format must be YYYY-MM-DD.
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD (e.g., 2026-10-22).")

    filter_query = create_filter(
        flights=[
            FlightQuery(
                date=date,
                from_airport=origin.upper().strip(),
                to_airport=destination.upper().strip(),
            )
        ],
        seat="economy",
        trip="one-way",
        passengers=Passengers(adults=1),
    )

    try:
        results = get_flights(filter_query)
    except Exception as e:
        return [{"error": f"Failed to fetch flights: {str(e)}"}]

    clean_results = []
    # Return top 5 matching flights
    for item in results[:5]:
        airlines = getattr(item, "airlines", ["Unknown"])
        raw_price = getattr(item, "price", 0.0)
        sub_flights = getattr(item, "flights", [])

        stops = len(sub_flights) - 1 if len(sub_flights) > 0 else 0
        total_duration = sum(getattr(f, "duration", 0) for f in sub_flights)

        clean_results.append({
            "airline": ", ".join(airlines) if isinstance(airlines, list) else str(airlines),
            "price": _clean_price(raw_price),
            "stops": stops,
            "duration_minutes": total_duration,
            "origin": origin.upper().strip(),
            "destination": destination.upper().strip(),
            "date": date,
        })

    # Sort so the cheapest option is always first in the list
    clean_results.sort(key=lambda x: x.get("price", float("inf")))
    return clean_results
