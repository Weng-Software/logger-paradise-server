import asyncio
import sys
import websockets
import os

from azure.messaging.webpubsubservice import WebPubSubServiceClient

async def connect(url):
    async with websockets.connect(url) as ws:
        print('connected')
        while True:
            print('Received message: ' + await ws.recv())

if __name__ == '__main__':

    if len(sys.argv) != 1:
        print(len(sys.argv))
        print('Usage: python subscribe.py')
        exit(1)

    connection_string = os.getenv('AZURE_STRING')
    if not connection_string:
        print(f'Error: AZURE_STRING environment variable not set.')
        exit(1)

    hub_name = "test1"

    service = WebPubSubServiceClient.from_connection_string(connection_string, hub=hub_name)
    token = service.get_client_access_token()

    try:
        asyncio.get_event_loop().run_until_complete(connect(token['url']))
    except KeyboardInterrupt:
        pass