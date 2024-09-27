import os
import threading
import time  # Ensure to import time for sleep functionality
from .client import create_client
from .api import NotPx
from .painter import painter
from .miner import mine_claimer
from .colors import Colors

def multithread_starter():
    session_files = [f for f in os.listdir("sessions/") if f.endswith(".session")]
    session_names = [f[:-8] for f in session_files]

    # Check if any session files were found
    if not session_files:
        print(f"[!] {Colors.YELLOW}No session files found in the 'sessions' directory.{Colors.END}")
        return  # Exit the function if no sessions are found

    max_retries = 3  # Maximum number of retries for loading each session

    for session_name in session_names:
        for attempt in range(max_retries):
            try:
                client = create_client(session_name)
                not_px_client = NotPx(client)
                threading.Thread(target=painter, args=[not_px_client, session_name]).start()
                threading.Thread(target=mine_claimer, args=[not_px_client, session_name]).start()
                break  # Exit retry loop on success
            except Exception as e:
                print(f"[!] {Colors.RED}Error on load session \"{session_name}\", attempt {attempt + 1}/{max_retries}, error: {e}{Colors.END}")
                if attempt < max_retries - 1:  # If not the last attempt, wait before retrying
                    time.sleep(5)  # Optional sleep before retrying
                else:
                    print(f"[!] {Colors.RED}All attempts failed for session \"{session_name}\".{Colors.END}")
