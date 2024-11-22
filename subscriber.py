import asyncio
import websockets
import os
from azure.messaging.webpubsubservice import WebPubSubServiceClient

class Subscriber:
    def __init__(self, hub_name):
        self.connection_string = os.getenv('AZURE_STRING')
        if not self.connection_string:
            raise ValueError("AZURE_STRING environment variable not set.")
        self.hub_name = hub_name
        self.service_client = None
        self.token = None

    def connect(self):
        self.service_client = WebPubSubServiceClient.from_connection_string(self.connection_string, hub=self.hub_name)
        self.token = self.service_client.get_client_access_token()
        print(f"Connected to hub '{self.hub_name}'. Token generated.")

    async def subscribe(self):
        if not self.token:
            raise ValueError("Subscriber is not connected. Call `connect()` first.")
        async with websockets.connect(self.token['url']) as ws:
            print("Connected to WebSocket")
            while True:
                message = await ws.recv()
                print(f"Received message: {message}")


if __name__ == '__main__':
    hub_name = "logger"
    subscriber = Subscriber(hub_name)
    subscriber.connect()

    try:
        asyncio.get_event_loop().run_until_complete(subscriber.subscribe())
    except KeyboardInterrupt:
        print("\nDisconnected from WebSocket.")
