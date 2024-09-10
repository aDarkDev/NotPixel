from telethon.sync import TelegramClient,functions
from urllib.parse import unquote
import threading
import requests
import urllib3
import random
import time

api_id = 123 # your api id
api_hash = "123" # your api hash
client = TelegramClient("NotPx_Auto",api_id,api_hash).start()
report_bug_text = "If you have done all the steps correctly and you think this is a bug, report it to github.com/aDarkDev with response. response: {}"
authenticate_error = "Please follow the steps correctly. Not authenticated."

def GetWebAppData():
    notcoin = client.get_entity("notpixel")
    msg = client(functions.messages.RequestWebViewRequest(notcoin,notcoin,platform="android",url="https://notpx.app/"))
    webappdata_global = msg.url.split('https://notpx.app/#tgWebAppData=')[1].replace("%3D","=").split('&tgWebAppVersion=')[0].replace("%26","&")
    user_data = webappdata_global.split("&user=")[1].split("&auth")[0]
    webappdata_global = webappdata_global.replace(user_data,unquote(user_data))
    return webappdata_global

class NotPx:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.__update_headers()

    def __update_headers(self):
        WebAppQuery = GetWebAppData()
        self.session.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Authorization': f'initData {WebAppQuery}',
            'Priority': 'u=1, i',
            'Referer': 'https://notpx.app/',
            'Sec-Ch-Ua': 'Chromium;v=119, Not?A_Brand;v=24',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': 'Linux',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.105 Safari/537.36',
        }

    def request(self,method,end_point,key_check,data=None):
        try:
            if method == "get":
                response = self.session.get(f"https://notpx.app/api/v1{end_point}",timeout=5)
                if response.status_code == 200:
                    if key_check in response.text:
                        json_response = response.json()
                        return json_response
                    else:
                        raise Exception(report_bug_text.format(response.text))
                else:
                    raise Exception(authenticate_error)
            else:
                response = self.session.post(f"https://notpx.app/api/v1{end_point}",timeout=5,json=data)
                if response.status_code == 200:
                    if key_check in response.text:
                        json_response = response.json()
                        return json_response
                    else:
                        raise Exception(report_bug_text.format(response.text))
                elif response.status_code >= 500:
                    time.sleep(5)
                    return self.request(method,end_point,key_check,data)
                else:
                    raise Exception(authenticate_error)
        except requests.exceptions.ConnectionError:
            print("[!] {}Requester{}: {}ConnectionError{} {}. Sleeping for 5s...".format(
                    Colors.CYAN,Colors.END,
                    Colors.RED,Colors.END,
                    end_point
                ))
            time.sleep(5)
        except urllib3.exceptions.NewConnectionError:
            print("[!] {}Requester{}: {}NewConnectionError{} {}. Sleeping for 5s...".format(
                    Colors.CYAN,Colors.END,
                    Colors.RED,Colors.END,
                    end_point
                ))
            time.sleep(5)
        except requests.exceptions.Timeout:
            print("[!] {}Requester{}: {}Timeout Error{} {}. Sleeping for 5s...".format(
                    Colors.CYAN,Colors.END,
                    Colors.RED,Colors.END,
                    end_point
                ))
            time.sleep(5)

    def claim_mining(self):
        return self.request("get","/mining/claim","claimed")['claimed']

    def accountStatus(self):
        return self.request("get","/mining/status","speedPerSecond")

    def paintPixel(self):
        # making pixel randomly
        colors = [ "#FFFFFF" , "#000000" , "#00CC78" , "#BE0039" ]
        random_pixel = (random.randint(100,990) * 1000) + random.randint(100,990)
        data = {"pixelId":random_pixel,"newColor":random.choice(colors)}

        return self.request("post","/repaint/start","balance",data)['balance']

class Colors:
    # Source: https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    # cancel SGR codes if we don't write to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        # set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32


print("""{}
 _   _       _  ______       ______       _   
| \ | |     | | | ___ \      | ___ \     | |  
|  \| | ___ | |_| |_/ /_  __ | |_/ / ___ | |_ 
| . ` |/ _ \| __|  __/\ \/ / | ___ \/ _ \| __|
| |\  | (_) | |_| |    >  <  | |_/ / (_) | |_ 
\_| \_/\___/ \__\_|   /_/\_\ \____/ \___/ \__|
                                              
        NotPx Auto Paint & Claim by aDarkDev - v0.2 {}\n""".format(Colors.BLUE,Colors.END))

NotPxClient = NotPx()

def painter():
    print("[+] {}Auto painting started{}.".format(Colors.CYAN,Colors.END))
    while True:
        try:
            charges = NotPxClient.accountStatus()['charges']
            if charges > 0:
                for _ in range(charges):
                    balance = NotPxClient.paintPixel()
                    print("[+] {}Painter{}: 1 {}Pixel painted{} successfully. User new balance: {}{}{}".format(
                        Colors.CYAN,Colors.END,
                        Colors.GREEN,Colors.END,
                        Colors.GREEN,balance,Colors.END
                    ))
                    t = random.randint(1,6)
                    print("[!] {}Painter anti-detect{}: Sleeping for {}...".format(Colors.CYAN,Colors.END,t))
                    time.sleep(t)
            else:
                print("[!] {}Painter{}: {}No charge aviable{}. Sleeping for 5 minutes...".format(
                    Colors.CYAN,Colors.END,
                    Colors.YELLOW,Colors.END
                ))
                time.sleep(300)
        except requests.exceptions.ConnectionError:
            print("[!] {}Painter{}: {}ConnectionError{}. Sleeping for 5s...".format(
                    Colors.CYAN,Colors.END,
                    Colors.RED,Colors.END
                ))
            time.sleep(5)
        except urllib3.exceptions.NewConnectionError:
            print("[!] {}Painter{}: {}NewConnectionError{}. Sleeping for 5s...".format(
                    Colors.CYAN,Colors.END,
                    Colors.RED,Colors.END
                ))
            time.sleep(5)
        except requests.exceptions.Timeout:
            print("[!] {}Painter{}: {}Timeout Error{}. Sleeping for 5s...".format(
                    Colors.CYAN,Colors.END,
                    Colors.RED,Colors.END
                ))
            time.sleep(5)
        
        
def mine_claimer():
    print("[+] {}Auto claiming started{}.".format(Colors.CYAN,Colors.END))
    while True:
        acc_data = NotPxClient.accountStatus()
        fromStart = acc_data['fromStart']
        speedPerSecond = acc_data['speedPerSecond']
        if fromStart * speedPerSecond > 2:
            claimed_count = round(NotPxClient.claim_mining(),2)
            print("[+] {}Miner{}: {} NotPx Token {}claimed{}.".format(
                Colors.CYAN,Colors.END,
                claimed_count,Colors.GREEN,Colors.END
            ))

        print("[!] {}Miner{}: Sleeping for 1 hour...".format(Colors.CYAN,Colors.END))
        time.sleep(3600)


# start script
if __name__ == "__main__":
    threading.Thread(target=painter).start()
    mine_claimer()
