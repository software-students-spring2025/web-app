import os
from dotenv import load_dotenv

load_dotenv()

DSN = os.getenv("DSN", "mongodb://localhost/new")
PORT = int(os.getenv("PORT", 3000))
