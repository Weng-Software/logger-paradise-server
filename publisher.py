from azure.messaging.webpubsubservice import WebPubSubServiceClient
import os

class Publisher:
    def __init__(self, hub_name):
        self.connection_string = os.getenv('AZURE_STRING')
        if not self.connection_string:
            raise ValueError("AZURE_STRING environment variable not set.")
        self.hub_name = hub_name
        self.service_client = None

    def connect(self):
        self.service_client = WebPubSubServiceClient.from_connection_string(self.connection_string, hub=self.hub_name)
        print(f"Connected to hub '{self.hub_name}'.")

    def publish(self, message):
        if not self.service_client:
            raise ValueError("Publisher is not connected. Call `connect()` first.")
        self.service_client.send_to_all(message, content_type='text/plain')
        print(f"Message sent: {message}")

# Example Usage
if __name__ == '__main__':
    hub_name = "logger"
    publisher = Publisher(hub_name)
    publisher.connect()
    publisher.publish("Hello from the Publisher!")