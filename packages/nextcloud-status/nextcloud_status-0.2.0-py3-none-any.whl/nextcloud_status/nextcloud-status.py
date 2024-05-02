#!env python3

import typer
import os
import configparser
from rich import print
from enum import Enum
import requests 
from requests.auth import HTTPBasicAuth
import sys
import json
from typing_extensions import Annotated
from datetime import datetime, timedelta

def get_emoji(emoji_code):
    """Return the emoji if it's in the list, otherwise None."""
    with open("gh_emoji.json", "r") as f:
        emoji_map = json.loads(f.read())
    return emoji_map.get(emoji_code)


class StatusEnum(str, Enum):
    online = "online"
    away = "away"
    dnd = "dnd"
    invisible = "busy"
    offline = "offline"

app = typer.Typer()

colours = {"online": "[bold green]", "away": "[bold yellow]", "dnd": "[bold blue]", "invisible": "[white]", "offline": "[gray]"}

"""
Convert a time string to a Unix timestamp for today or tomorrow, for specifying
message timeout.
"""
def time_to_future_timestamp(time_str):
    # Parse the time string into a datetime object for today.
    future_time = datetime.strptime(time_str, "%H:%M").replace(
        year=datetime.now().year, 
        month=datetime.now().month, 
        day=datetime.now().day
    )

    # Check if the parsed time is already past today. If so, add a day.
    if future_time <= datetime.now():
        future_time += timedelta(days=1)

    # Convert the datetime object to a Unix timestamp.
    return int(future_time.timestamp())

def get_config_path():
    # Determine the OS-specific path to the config file.
    home = os.path.expanduser("~")
    if os.name == 'posix':  # Linux, macOS, etc.
        config_path = os.path.join(home, ".config", "nextcloud-status", "config.cfg")
    elif os.name == 'nt':  # Windows
        config_path = os.path.join(home, "AppData", "Local", "nextcloud-status", "config.cfg")
    else:
        raise Exception("Unsupported operating system.")
    return config_path

def read_config(config_path):
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
        return config
    else:
        return None

def write_config(config_path, url, username, password):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'url': url,
        'username': username,
        'password': password
    }
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as configfile:
        config.write(configfile)

def get_config():
    config_path = get_config_path()
    config = read_config(config_path)

    if config and 'DEFAULT' in config:
        url = config['DEFAULT']['url']
        username = config['DEFAULT']['username']
        password = config['DEFAULT']['password']
    else:
        print("[bold white]Your NextCloud configuration[/bold white]")
        url = typer.prompt("Enter NextCloud server URL")
        username = typer.prompt("Enter your username")
        password = typer.prompt("Enter your password (hidden)", hide_input=True)
        write_config(config_path, url, username, password)

    return {"url": url, "username": username, "password": password}


def update_status(server_url, username, app_token, status_type="online", status_msg=None, icon=None, expiry_time=None):
    url = f"{server_url}/ocs/v2.php/apps/user_status/api/v1/user_status/status"
    headers = {
        'OCS-APIRequest': 'true',
        'Content-Type': 'application/json'
    }
    data = {
        'statusType': status_type
    }
    response = requests.put(url, json=data, auth=HTTPBasicAuth(username, app_token), headers=headers)
    if response.status_code != 200:
        print(f"[red]Failed to update status:[/red] {response.text}")
        sys.exit(1)
    data = {}

    url = f"{server_url}/ocs/v2.php/apps/user_status/api/v1/user_status/message/custom"
    if status_msg:
        data['message'] = status_msg
        if expiry_time is not None:
            try:
                data['clearAt'] = time_to_future_timestamp(expiry_time)
            except:
                print(f"[bold red]Bad time format. Use HH:MM[/bold red]")
                return 1
    if not icon:
        icon = None
    else:
        if len(icon) > 1:
            if icon[0] == ":" and icon[-1] == ":":
                icon = get_emoji(icon)
                if icon is None:
                    print("[red]Emoji not found.")
                    return
                else:
                    data['statusIcon'] = icon
            else:
                print("[red]Icon must be a single character emoji.")
                return
        data['statusIcon'] = icon
    response = requests.put(url, json=data, auth=HTTPBasicAuth(username, app_token), headers=headers)
    if response.status_code == 200:
        print("[green]Status updated successfully")
    else:
        print(f"[red]Failed to update status:[/red] {response.text}")
        sys.exit(1)


@app.command()
def set_status(status: StatusEnum, 
               message: Annotated[str, typer.Option(help="Status message string")] = None, 
               icon: Annotated[str, typer.Option(help="An emoji or github markup like :smile:")]= None, 
               clear_at: Annotated[str, typer.Option(help="Time to clear the status message, in 'HH:MM' format.")] = None):
    """
    Set your NextCloud status.
    
    """
    if not status and not message and not icon:
        print("No status, message, or icon provided.")
        return
    config = get_config()
    update_status(config['url'], config['username'], config['password'], 
                  status_type=status, status_msg=message, icon=icon, expiry_time=clear_at)
    

@app.command()
def get_status():
    """
    Get the current status from the server.
    """
    config = get_config()
    username, app_token, url = config['username'], config['password'], config['url']
    url = f"{url}/ocs/v2.php/apps/user_status/api/v1/user_status"
    headers = {
        'OCS-APIRequest': 'true',
        'Accept': 'application/json'
    }
    response = requests.get(url, auth=HTTPBasicAuth(username, app_token), headers=headers)
    if response.status_code == 200:
        status_data = response.json()['ocs']['data']
        print(f"{colours[status_data['status']]}{status_data['status']}[/]  {status_data['message']} {status_data['icon']}")
    else:
        print(f"Failed to fetch status, or no status set: {response.text}")

def main():
    app()

# if __name__ == "__main__":
    # app()

