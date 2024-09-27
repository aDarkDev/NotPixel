import time
from .api import NotPx
from .colors import Colors

def mine_claimer(not_px_client, session_name):
    time.sleep(5)  # Start with delay
    print(f"[+] {Colors.CYAN}{session_name}{Colors.END}: Auto claiming started.")

    while True:
        acc_data = not_px_client.account_status()  # Attempt to get account status once

        if acc_data is None:
            print(f"[!] {Colors.CYAN}{session_name}{Colors.END}: {Colors.RED}Failed to retrieve account status. Retrying in 5 seconds...{Colors.END}")
            time.sleep(5)  # Wait before retrying
            continue  # Retry on failure
        
        if 'fromStart' in acc_data and 'speedPerSecond' in acc_data:
            if acc_data['fromStart'] * acc_data['speedPerSecond'] > 0.3:
                claimed_count = round(not_px_client.claim_mining(), 2)
                print(f"[+] {Colors.CYAN}{session_name}{Colors.END}: NotPx Token {claimed_count} claimed.")
            else:
                print(f"[!] {Colors.CYAN}{session_name}{Colors.END}: {Colors.YELLOW}Insufficient speed for claiming. Waiting for 10 minutes...{Colors.END}")
                time.sleep(600)  # Sleep for 10 minutes if no charges are available
        else:
            print(f"[!] {Colors.CYAN}{session_name}{Colors.END}: {Colors.RED}Unexpected account data format. Retrying in 5 seconds...{Colors.END}")
            time.sleep(5)  # Wait before retrying

        print(f"[!] {Colors.CYAN}{session_name}{Colors.END}: Sleeping for 1 hour...")
        time.sleep(3600)  # Sleep for 1 hour before the next attempt
