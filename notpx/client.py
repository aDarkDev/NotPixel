from telethon.sync import TelegramClient
from .config import API_ID, API_HASH
import time

def create_client(session_name, max_retries=3):
    """Create and return a Telegram client with retry logic."""
    for attempt in range(max_retries):
        try:
            client = TelegramClient(f"sessions/{session_name}", API_ID, API_HASH).start()
            return client  # Return the client if successful
        except Exception as e:
            print(f"[!] Attempt {attempt + 1}/{max_retries} failed to create client for session \"{session_name}\": {e}")
            if attempt < max_retries - 1:  # If not the last attempt, wait before retrying
                time.sleep(5)  # Optional sleep before retrying
            else:
                print(f"[!] {Colors.RED}All attempts failed for session \"{session_name}\". Unable to create client.{Colors.END}")
    return None  # Return None if all attempts fail
