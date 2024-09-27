import os
from notpx.colors import Colors
from notpx.utils import multithread_starter
from notpx.client import create_client

def main():
    if not os.path.exists("sessions"):
        os.mkdir("sessions")

    while True:
        option = input(f"[!] {Colors.BLUE}Enter 1{Colors.END} For Adding Account and {Colors.BLUE}2 for start{Colors.END} mine + claim: ")
        if option == "1":
            name = input("\nEnter Session name: ")
            if not any(name in f for f in os.listdir("sessions/")):
                client = create_client(name)
                client.disconnect()
                print(f"[+] Session {name} {Colors.GREEN}saved successfully.{Colors.END}")
            else:
                print(f"[x] Session {name} {Colors.RED}already exists.{Colors.END}")
        elif option == "2":
            print(f"{Colors.YELLOW}Warning! Most airdrops utilize UTC detection to prevent cheating.{Colors.END}")
            multithread_starter()
            break

if __name__ == "__main__":
    print(r"""{} 
    _   _       _  ______       ______       _   
    | \ | |     | | | ___ \      | ___ \     | |  
    |  \| | ___ | |_| |_/ /_  __ | |_/ / ___ | |_ 
    | . ` |/ _ \| __|  __/\ \/ / | ___ \/ _ \| __|
    | |\  | (_) | |_| |    >  <  | |_/ / (_) | |_ 
    \_| \_/\___/ \__\_|   /_/\_\ \____/ \___/ \__|
                                                
            NotPx Auto Paint & Claim by aDarkDev - v1.5 {}
    """.format(Colors.BLUE, Colors.END))
    main()
