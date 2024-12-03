from azure.messaging.webpubsubservice import WebPubSubServiceClient
import os
from flask import Flask, jsonify
from log_generator import LogGenerator
from log_reader import LogReader

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

    def publish_log(self, log):
        if not self.service_client:
            raise ValueError("Publisher is not connected. Call `connect()` first.")
        self.service_client.send_to_all(str(log), content_type='text/plain')
        print(f"Published Log: {log}")


# Flask app to serve the connection string
app = Flask(__name__)

# Flask route to provide the connection string
@app.route('/connection-string', methods=['GET'])
def get_connection_string():
    connection_string = os.getenv('AZURE_STRING')
    if not connection_string:
        return jsonify({'error': 'AZURE_STRING environment variable not set'}), 500
    return jsonify({'connection_string': connection_string})

# Example Usage
if __name__ == '__main__':
    hub_name = "logger"
    publisher = Publisher(hub_name)
    publisher.connect()

    # Generate logs and simulate log reading
    generator = LogGenerator(num_logs=100, timespan_minutes=10)
    logs = generator.generate_logs()

    reader = LogReader(logs, publisher, speedup_factor=60)
    print("Starting log reader...")
    reader.read_logs()

    app.run(debug=True)