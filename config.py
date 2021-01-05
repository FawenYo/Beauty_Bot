import os
import pymongo

from rich.console import Console
from dotenv import load_dotenv

load_dotenv()
console = Console()

PTT_URL = "https://www.ptt.cc"

# LINE Bot
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# MongoDB
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PWD = os.environ.get("MONGO_PWD")

client = pymongo.MongoClient(
    f"mongodb+srv://{MONGO_USER}:{MONGO_PWD}@cluster0.mgk18.mongodb.net/<dbname>?retryWrites=true&w=majority"
)
db = client.db