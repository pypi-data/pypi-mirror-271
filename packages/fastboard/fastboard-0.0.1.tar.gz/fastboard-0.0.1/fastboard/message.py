from .config import configdb
import requests

"""def send_channel_message(channel_id:int):
    token = configdb['BOT_TOKEN']
    json = {
        "embeds": [{
            "title": "NIGER",
            "description": "NIGER",
            "color": 0x707070,
            "fields": [{
                "name": "hm",
                "value": "NIGER",
                "inline": False
            }]
  }]
}
    r = requests.post(f"https://discord.com/api/v6/channels/{channel_id}/messages", headers={"Authorization": f"Bot {token}"}, json=json)
    r.raise_for_status()
    return r.json()"""