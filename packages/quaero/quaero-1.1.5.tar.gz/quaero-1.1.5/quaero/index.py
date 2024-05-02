#!/usr/bin/env python3

import argparse
import os
import asyncio
import signal
import sys
from colorama import Fore, Style
import time
import json

from quaero.openai import fetch_data
from quaero.utils import print_waiting, save_to_file, check_for_config
from quaero.consts import app_directory, api_key_key, config_path

async def main_impl():
    conversation = {}
    model = 'gpt-3.5-turbo'

    
    # Handler for ?? (ctrl + c)
    def quit_handler(sig, frame):
        print("\nExiting script...")
        id = save_to_file(conversation)
        if id:
            print("Conversation ID: ", id)
        sys.exit(0)

    signal.signal(signal.SIGINT, quit_handler)

    parser = argparse.ArgumentParser(description="🤖 ChatGPT CLI")
    parser.add_argument(
        "command", choices=["init"], help="Set up your OpenAI credentials", nargs="?"
    )
    parser.add_argument(
        "-c", "--conversation", help="Use with the ID printed at the end of a previous conversation to resume that same conversation.  Will not work if the conversation has been deleted.", nargs=1
    )
    parser.add_argument(
        "-m", "--model", help="Specify which model to use. Options are -m 3: gpt-3.5-turbo and -m 4: gpt-4-turbo-preview.  Will default to gpt-3.5-turbo unless -m 4 is passed.", nargs=1
    )
    args = parser.parse_args()

    # Handle init setup
    if args.command == "init":
        print(
            Fore.YELLOW + "Welcome to quaero! To get started you will need to generate an OpenAI API key and paste it here to save it to your quaero config.\n\nVisit " + Fore.WHITE + "https://platform.openai.com/api-keys." + Fore.YELLOW + "\n\nThe key should be like sk-{20chars}\n" + Style.RESET_ALL
        )
        key = input("Please paste your key: ")
        os.makedirs(app_directory, exist_ok=True)
        with open(config_path, "w+") as file:
            file.write(f"{api_key_key}={key.strip()}")
        print("Success!  You are ready to ask your first question.")

    # Make sure an API key is set
    try:
        check_for_config()
    except Exception as e:
        print(Fore.RED, e, Style.RESET_ALL)
        sys.exit(1)

    # TODO: clean out old conversations
        
    if args.conversation:
        d, t = args.conversation[0].split('/')
        conversation_path = os.path.join(app_directory, d, t)
        if not os.path.isfile(conversation_path):
            print(Fore.RED + "That conversation ID was not found" + Style.RESET_ALL)
            sys.exit(1)
        with open(conversation_path) as file:
            conversation = json.load(file)

    if args.model:
        model_arg = args.model[0]
        if model_arg == '4':
            model = 'gpt-4-turbo-preview'
        elif model_arg == '3':
            # already set as the default
            pass
        else:
            raise Exception('Unrecognised model input.  Options are 3 for 3.5-turbo (default) or 4 for 4-turbo-preview.')

    while True:
        fetched_data_flag = asyncio.Event()

        # Prompt user for their question
        user_input = input("> ")

        # Store their question in the conversation dictionary
        conversation[time.time()] = {'content': user_input, 'role': 'user'}

        # Simultaneous kick off the API request and printing the waiting message
        # The fetch_data function also writes the response to the conversation dictionary
        await asyncio.gather(
            fetch_data(conversation, model, fetched_data_flag), print_waiting(fetched_data_flag)
        )

        print("\n")


def main():
    # Asyncio lib needed so the data request and wait message can happen simultaneously (requests lib is blocking)
    asyncio.run(main_impl())


if __name__ == "__main__":
    main()
