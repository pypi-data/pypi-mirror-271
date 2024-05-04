import json
import requests
from .config import configdb

def get_roles(guild_id: int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v6/guilds/{guild_id}/roles", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()
    return r.json()


def add_member_role(guild_id:int, user_id:int, role_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.put(f"https://discord.com/api/v8/guilds/{guild_id}/members/{user_id}/roles/{role_id}", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()


def create_guild_role(guild_id:int, name:str):
    token = configdb['BOT_TOKEN']
    json = {
        "name": name
    }
    r = requests.post(f"https://discord.com/api/v8/guilds/{guild_id}/roles", headers={"Authorization": f"Bot {token}"},json=json)
    r.raise_for_status()


def remove_member_role(guild_id:int, user_id:int, role_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.delete(f"https://discord.com/api/v8/guilds/{guild_id}/members/{user_id}/roles/{role_id}", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()


def delete_guild_role(guild_id:int, role_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.delete(f"https://discord.com/api/v8/guilds/{guild_id}/roles/{role_id}", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()   