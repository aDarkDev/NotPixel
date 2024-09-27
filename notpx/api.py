import requests
from urllib.parse import unquote
from telethon import functions
from .config import WEB_APP_URL
import random
import time
import urllib3

class NotPx:
    def __init__(self, client):
        self.client = client
        self.session = requests.Session()
        self.update_headers()

    def update_headers(self):
        web_app_data = self.get_web_app_data()
        self.session.headers.update({
            'Authorization': f'initData {web_app_data}',
        })

    def get_web_app_data(self):
        notcoin = self.client.get_entity("notpixel")
        msg = self.client(functions.messages.RequestWebViewRequest(notcoin, notcoin, platform="android", url=WEB_APP_URL))
        webappdata_global = msg.url.split('https://notpx.app/#tgWebAppData=')[1].replace("%3D", "=").split('&tgWebAppVersion=')[0].replace("%26", "&")
        user_data = webappdata_global.split("&user=")[1].split("&auth")[0]
        return webappdata_global.replace(user_data, unquote(user_data))

    def request(self, method, end_point, key_check, data=None):
        url = f"{WEB_APP_URL}/api/v1{end_point}"
        
        while True:  # Using while loop to handle the request
            try:
                response = self.session.request(method, url, json=data, timeout=5)
                return self.handle_response(response, key_check, method, end_point, data)
            except (requests.exceptions.ConnectionError, 
                    urllib3.exceptions.NewConnectionError, 
                    requests.exceptions.Timeout) as e:
                # Handle connection errors silently, continue to retry
                # print(f"[!] Connection error occurred: {e}. Please check your internet connection.")
                continue
            except requests.exceptions.HTTPError as e:
                # Handle HTTP errors silently, continue to retry
                # print(f"[!] HTTP error occurred: {e}. Status Code: {e.response.status_code}")
                continue
            except Exception as e:
                # Handle unexpected errors silently, continue to retry
                # print(f"[!] An unexpected error occurred: {e}. No further attempts will be made.")
                continue

        return None  # Return None if the request fails

    def handle_response(self, response, key_check, method, end_point, data):
        if response.status_code == 200:
            response_json = response.json()
            if key_check in response_json:
                return response_json
            else:
                raise ValueError(f"Key '{key_check}' not found in response: {response.text}")
        elif response.status_code >= 500:
            time.sleep(5)
            return self.request(method, end_point, key_check, data)  # Retry on server error
        else:
            self.update_headers()
            print("[+] Authentication renewed!")

    def claim_mining(self):
        return self.request("get", "/mining/claim", "claimed")['claimed']

    def account_status(self):
        return self.request("get", "/mining/status", "speedPerSecond")

    def auto_paint_pixel(self):
        colors = ["#FFFFFF", "#000000", "#00CC78", "#BE0039"]
        random_pixel = (random.randint(100, 990) * 1000) + random.randint(100, 990)
        data = {"pixelId": random_pixel, "newColor": random.choice(colors)}
        response = self.request("post", "/repaint/start", "balance", data)

        if response and 'balance' in response:
            return response['balance']
        print("[!] Failed to paint pixel, no valid response. Retrying...")
        return None

    def paint_pixel(self, x, y, hex_color):
        pixel_formatted = (y * 1000) + x + 1
        data = {"pixelId": pixel_formatted, "newColor": hex_color}
        return self.request("post", "/repaint/start", "balance", data)['balance']
