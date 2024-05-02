import json
import aiohttp
from quaero.utils import get_api_key
from colorama import Style
import time

# Fn to call the bot and print its response as it streams in
async def fetch_data(conversation, model, fetched_data_flag):
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}", "content-type": "application/json"}
    url = f"https://api.openai.com/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [value for value in conversation.values()],
        "temperature": 0.7,
        "stream": True,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, data=json.dumps(payload), headers=headers
            ) as response:
                if response.status == 200:
                    # Response received - can stop printing the 'Thinking...' message
                    fetched_data_flag.set()
                    timestamp = time.time()
                    whole_response = []

                    print(Style.RESET_ALL, "\n\n> 🤖")
                    # The streaming response is SSEs - process each event by iterating through the chunks,
                    # instead of waiting for the whole request to finish
                    # https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
                    async for chunk in response.content:
                        try:
                            parsed = json.loads(chunk.decode("utf-8").removeprefix("data: "))
                            # TODO: validate that the event looks like what you expect, and handle better if not
                            chunk_message = parsed["choices"][0]["delta"]["content"]
                            # TODO: just have a string that gets longer?
                            # Append each chunk to a list that will be added to the conversation object
                            whole_response.append(chunk_message)
                            print(chunk_message, end="", flush=True)
                        except:
                            pass
                    conversation[f"{timestamp}-bot"] = {'content': "".join(whole_response), 'role': 'assistant'}
                else:
                    print(f"Error calling OpenAI.  API response: {response.status}")
    except aiohttp.ClientError as e:
        print(f"An error occured: {e}")