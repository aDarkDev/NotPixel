import random
import time
from .api import NotPx
from .colors import Colors

def painter(not_px_client, session_name):
    print(f"[+] {Colors.CYAN}{session_name}{Colors.END}: Auto painting started{Colors.END}.")
    
    while True:
        charges = not_px_client.account_status()  # Get account status
        if not charges:
            time.sleep(5)  # Wait before retrying
            continue

        charges = charges.get('charges', 0)
        if charges > 0:
            for _ in range(charges):
                balance = not_px_client.auto_paint_pixel()  # Attempt to paint a pixel
                if balance is not None:
                    print(f"[+] {Colors.CYAN}{session_name}{Colors.END}: {Colors.GREEN}Pixel painted successfully. User new balance: {balance}{Colors.END}")
                else:
                    print(f"[!] {Colors.RED}Painting failed.{Colors.END}")  # Log a failure without retrying
                time.sleep(random.randint(1, 6))  # Sleep between each pixel painting
        else:
            print(f"[!] {Colors.CYAN}{session_name}{Colors.END}: {Colors.YELLOW}No charge available. Sleeping for 10 minutes...{Colors.END}")
            time.sleep(600)  # Sleep for 10 minutes if no charges are available
