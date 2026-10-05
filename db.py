import os
from typing import Any, Dict, List
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Check common environment variable names with local fallback
mongo_uri = (
    os.getenv("MONGODB_URI")
    or os.getenv("MONGO_URI")
    or "mongodb://localhost:27017/"
)
db_name = os.getenv("DB_NAME", "flight_tracker_test")

# 5-second timeout prevents indefinite hangs on network drops
client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
db = client[db_name]
flights_collection = db["saved_flights"]


def save_flight(flight_data: Dict[str, Any]) -> str:
    """Inserts a flight document into the database."""
    if not isinstance(flight_data, dict) or not flight_data:
        raise ValueError("Flight data must be a non-empty dictionary.")

    result = flights_collection.insert_one(flight_data)
    return str(result.inserted_id)


def list_saved_flights(limit: int = 10) -> List[Dict[str, Any]]:
    """Returns saved flights, converting ObjectId to string for JSON serialization."""
    docs = list(flights_collection.find().limit(limit))
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    return docs


def update_saved_flight(flight_id: str, update_fields: Dict[str, Any]) -> bool:
    """Updates fields of a saved flight document by its ID."""
    if not ObjectId.is_valid(flight_id):
        raise ValueError(f"Invalid flight ID format: {flight_id}")
    if not update_fields:
        raise ValueError("Update fields cannot be empty.")

    result = flights_collection.update_one(
        {"_id": ObjectId(flight_id)},
        {"$set": update_fields}
    )
    return result.matched_count > 0


def delete_saved_flight(flight_id: str, confirm: bool = False) -> str:
    """Deletes a single flight document. Requires explicit confirm=True."""
    if not confirm:
        return "Action aborted: confirm=True is required to delete a flight."
    if not ObjectId.is_valid(flight_id):
        raise ValueError(f"Invalid flight ID format: {flight_id}")

    result = flights_collection.delete_one({"_id": ObjectId(flight_id)})
    if result.deleted_count > 0:
        return f"Flight {flight_id} deleted successfully."
    return f"No flight found with ID {flight_id}."


def drop_collection(confirm: bool = False) -> str:
    """Drops the entire saved_flights collection. Requires explicit confirm=True."""
    if not confirm:
        return "Action aborted: confirm=True is required to drop the collection."

    flights_collection.drop()
    return "Collection 'saved_flights' dropped successfully."