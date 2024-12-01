import asyncio
import websockets
from azure.messaging.webpubsubservice import WebPubSubServiceClient
import requests

class Subscriber:
    def __init__(self, hub_name):
        self.connection_string = None
        self.hub_name = hub_name
        self.service_client = None
        self.token = None

    def fetch_connection_string(self, api_url):
        """Fetch the connection string from the Flask API."""
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            self.connection_string = response.json().get('connection_string')
            if not self.connection_string:
                raise ValueError("Connection string not found in API response.")
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch connection string: {e}")
        
    def connect(self):
        if not self.connection_string:
            raise ValueError("Connection string is not set. Fetch it first using `fetch_connection_string()`.")
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
    flask_api_url = "http://127.0.0.1:5000/connection-string" 
    hub_name = "logger"
    subscriber = Subscriber(hub_name)
    subscriber.fetch_connection_string(flask_api_url)
    subscriber.connect()

    try:
        asyncio.run(subscriber.subscribe())
    except KeyboardInterrupt:
        print("\nDisconnected from WebSocket.")
