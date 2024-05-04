import requests
from .config import configdb

def guilds_data(guilds_id:int):
    token = configdb['BOT_TOKEN']
    resp = requests.get(f"https://discord.com/api/v6/guilds/{guilds_id}", headers={"Authorization": f"Bot {token}"})
    resp.raise_for_status()
    return resp.json()


def get_emojis(guild_id: int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v6/guilds/{guild_id}/emojis", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()
    return r.json()


def get_bans(guild_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v8/guilds/{guild_id}/bans", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()
    return r.json()


def create_ban(guild_id:int, user_id:int, delete_message_days:int ,reason:str):
    if delete_message_days > 7:
        delete_message_days = 7
    if len(reason) == 0:
        reason = "None"
    token = configdb['BOT_TOKEN']
    json = {
        "delete_message_days": delete_message_days,
        "reason": reason
    }
    r = requests.put(f"https://discord.com/api/v8/guilds/{guild_id}/bans/{user_id}", headers={"Authorization": f"Bot {token}"}, json=json)
    r.raise_for_status()


def remove_ban(guild_id:int, user_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.delete(f"https://discord.com/api/v8/guilds/{guild_id}/bans/{user_id}", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()


def get_guild_member(guild_id:int, user_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v8/guilds/{guild_id}/members/{user_id}", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()    
    return r.json()


def get_list_members(guild_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v8/guilds/{guild_id}/members", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()
    return r.json()


def remove_guild_member(guild_id:int, user_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.delete(f"https://discord.com/api/v8/guilds/{guild_id}/members/{user_id}", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()    


def get_guild_voice_regions(guild_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v8/guilds/{guild_id}/regions", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()     
    return r.json()


def get_guild_welcome_screen(guild_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v8/guilds/{guild_id}/welcome-screen", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()     
    return r.json()