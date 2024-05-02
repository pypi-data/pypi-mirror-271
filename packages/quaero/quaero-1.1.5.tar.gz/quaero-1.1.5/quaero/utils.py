from dotenv import dotenv_values, find_dotenv
import os
from colorama import Fore, Style
import asyncio
import datetime
import json

from quaero.consts import config_path, api_key_key, app_directory

def check_for_config():
    # TODO: specifically check for existence of file rather than keys?
    config = get_config()
    if not config.get("API_KEY", None):
        raise Exception("Config not set up properly.  Have you run `quaero init`?")


def get_config():
    return dotenv_values(config_path)


def get_api_key():
    config = get_config()
    api_key = config.get(api_key_key, None)
    if api_key == None:
        print(Fore.RED + "Unable to find API key.  Have you created run `quaero init`?" + Style.RESET_ALL)
        return
    return api_key


# Print message while waiting for data to be returned, to show that something is happening
async def print_waiting(fetched_data):
    print(Fore.YELLOW + "\nThinking...", end="")
    while not fetched_data.is_set():
        print(".", end="", flush=True)
        await asyncio.sleep(0.5)
    print(Style.RESET_ALL)

# Save conversation so it can be resumed or revisited
def save_to_file(output):
    if len(output.keys()):
        current_datetime = datetime.datetime.now()
        date, time = current_datetime.strftime("%Y%m%d"), current_datetime.strftime(
            "%H%M%S"
        )
        output_directory = os.path.join(app_directory, date)
        os.makedirs(output_directory, exist_ok=True)
        file_path = os.path.join(output_directory, time)
        with open(file_path, "w+") as file:
            file.write(json.dumps(output))
        return f"{date}/{time}"
