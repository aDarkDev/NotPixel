import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
WEB_APP_URL = "https://notpx.app/"
