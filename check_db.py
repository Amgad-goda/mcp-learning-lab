# check_db.py
from db import flights_collection, client, db_name

try:
    client.admin.command("ping")
    print(f"✅ Connected to MongoDB Atlas! Active DB: '{db_name}'")
    
    total = flights_collection.count_documents({})
    print(f"📦 Total saved flights: {total}\n")

    for i, doc in enumerate(flights_collection.find(), 1):
        print(f"[{i}] {doc}")

except Exception as e:
    print(f"❌ Connection error: {e}")