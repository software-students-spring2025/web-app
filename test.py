from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId

# Assuming you're using MongoDB and connected via pymongo
client = MongoClient('mongodb+srv://mlkelly:vicky1031@cluster0.82hw9.mongodb.net/myDatabase?retryWrites=true&w=majority')
db = client["myDatabase"]

# Sample data to test
exhibit_data = {
    "Exhibition Title": "Modern Art Exhibition",
    "Dates": {"start": "2025-03-01", "end": "2025-03-15"},
    "Location": "Art Gallery A",
    "Cost": 20,
    "Artist": "John Doe",
    "Art Style": "Abstract",
    "Art Medium": "Oil on Canvas",
    "Event Type": "Public",
    "Description": "An amazing modern art exhibition.",
    "Image_url": "http://example.com/image.jpg",
    "Created_by": "admin",
    "created_at": datetime.datetime.utcnow(),
}

# Insert exhibition to test create functionality
def test_create_exhibit():
    result = db.exhibits.insert_one(exhibit_data)
    print(f"Inserted exhibition with ID: {result.inserted_id}")
    return result.inserted_id

# Retrieve the exhibition to test reading functionality
def test_read_exhibit(exhibit_id):
    exhibit = db.exhibits.find_one({"_id": ObjectId(exhibit_id)})
    print(f"Exhibit details: {exhibit}")
    return exhibit

# Update the exhibition details to test update functionality
def test_update_exhibit(exhibit_id):
    updated_data = {
        "Exhibition Title": "Updated Modern Art Exhibition",
        "Location": "Art Gallery B",
        "Cost": 30
    }
    db.exhibits.update_one({"_id": ObjectId(exhibit_id)}, {"$set": updated_data})
    print(f"Exhibit with ID: {exhibit_id} updated.")
    return test_read_exhibit(exhibit_id)

# Delete the exhibition to test delete functionality
def test_delete_exhibit(exhibit_id):
    db.exhibits.delete_one({"_id": ObjectId(exhibit_id)})
    print(f"Exhibit with ID: {exhibit_id} deleted.")
    return db.exhibits.find_one({"_id": ObjectId(exhibit_id)}) is None

# Example of running tests:
exhibit_id = test_create_exhibit()  # First, create an exhibit
test_read_exhibit(exhibit_id)  # Then, read it back
test_update_exhibit(exhibit_id)  # Now, update it
test_delete_exhibit(exhibit_id)  # Finally, delete it
