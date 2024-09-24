# NotPixel
Introducing the [NotPixel Bot](https://t.me/notpixel): 

a fully automatic tool for claiming and painting. With built-in anti-detection features, it works efficiently and discreetly to get the best results. Simplify your tasks with the NotPixel Bot!
![d](https://github.com/aDarkDev/NotPixel/blob/3478a347a2783afbe5faff49672c4bead56d9907/shot.png)

## Features:
* 👾 Multi-Session ( New Update )
* 🔥 Multi-Thread  ( New Update )
* ⭕️ Error handling  ( New Update )
* ✍🏻 Draw with desired x,y ( New Update )
* 💰 Claim Mining
* 💰 Paint Pixel
* 💸 Show user balance
* 🤖 Anti detect
* 🐍 easy to use as module

Upcoming features: `Level Up` and `Boosts`.

## Installation

install telethon library to get `webappdata`
```bash
$ pip3 install telethon
```

edit line 
```python3
api_id = 123 # your api id
api_hash = "123" # your api hash
```
include your `API Hash` and `API ID`, which can be obtained from [my.telegram.org](https://my.telegram.org) under the Development section.

then just run it!
```bash
$ python3 main.py
```

## Using as Module:
Example:
```python3
from telethon import TelegramClient
from NotPixel import NotPx


api_id = 123 # your api id
api_hash = "123" # your api hash

client = TelegramClient("my_session",api_id,api_hash).start()
NotPx_client = NotPx(client)
NotPx_client.accountStatus()
NotPx_client.paintPixel(...)
NotPx_client.claim_mining(...)
NotPx_client.request(...)
```

### Don't forget to star⭐️ the project and report any bugs🪲 you encounter. Good luck!
