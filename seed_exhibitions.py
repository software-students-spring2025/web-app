import os
import pymongo
import datetime
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DBNAME")]
exhibitions_collection = db["exhibitions"]

# Sample exhibition data
sample_exhibitions = [
    {
        "title": "Dreamscapes: An Impressionist Journey",
        "dates": {
            "start": "2025-03-15",
            "end": "2025-04-30"
        },
        "location": "ArtSpace Gallery, New York",
        "cost": 15.00,
        "artist": {
            "name": "Alice Monet",
            "profile_url": "https://artistportfolio.com/alice-monet"
        },
        "art_style": "Impressionist",
        "art_medium": "Paintings",
        "event_type": "Launch Party",
        "description": "A mesmerizing collection of impressionist landscapes.",
        "image_url": "https://example.com/exhibition1.jpg",
        "created_by": "alice_monet",  # Track the artist who created it
        "created_at": datetime.datetime.utcnow()
    },
    {
        "title": "Neon Realities",
        "dates": {
            "start": "2025-04-10",
            "end": "2025-05-25"
        },
        "location": "Downtown Arts Hub, LA",
        "cost": 20.00,
        "artist": {
            "name": "Leo Stark",
            "profile_url": "https://artistportfolio.com/leo-stark"
        },
        "art_style": "Modern",
        "art_medium": "Digital Art",
        "event_type": "Pop-up",
        "description": "A deep dive into neon-inspired digital artworks.",
        "image_url": "",
        "created_by": "leo_stark",
        "created_at": datetime.datetime.utcnow()
    },
    {
        "title": "Abstract Wonders",
        "dates": {
            "start": "2025-02-01",
            "end": "2025-02-28"
        },
        "location": "Gallery 77, Chicago",
        "cost": 10.00,
        "artist": {
            "name": "Samantha Raye",
            "profile_url": "https://artistportfolio.com/samantha-raye"
        },
        "art_style": "Abstract",
        "art_medium": "Mixed Media",
        "event_type": "Exhibition",
        "description": "A collection of abstract mixed-media masterpieces.",
        "image_url": "https://example.com/exhibition3.jpg",
        "created_by": "samantha_raye",
        "created_at": datetime.datetime.utcnow()
    }
]

# Insert into MongoDB
exhibitions_collection.insert_many(sample_exhibitions)
print("Sample exhibitions inserted successfully!")
