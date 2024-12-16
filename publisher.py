from azure.messaging.webpubsubservice import WebPubSubServiceClient
import os
from flask import Flask, jsonify
from log_generator import LogGenerator
from log_reader import LogReader
from dotenv import load_dotenv
import os
import threading, time

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
        self.service_client.send_to_all(log.__dict__, content_type='application/json')
        print(f"Published Log: {log}")


# Flask app to serve the connection string
app = Flask(__name__)

# Flask route to provide the connection string
@app.route('/connection-string', methods=['GET'])
def get_connection_string():
    """Return the connection string as JSON."""
    connection_string = os.getenv('AZURE_STRING')
    if not connection_string:
        return jsonify({'error': 'AZURE_STRING environment variable not set'}), 500
    return jsonify({'connection_string': connection_string})


def start_flask():
    """Start the Flask server."""
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)


def start_log_reader(publisher):
    """Generate logs and read them."""
    load_dotenv()
    NUM_LOGS = int(os.getenv("NUM_LOGS", 100))
    TIMESPAN_MINUTES = int(os.getenv("TIMESPAN_MINUTES", 10))
    SPEEDUP_FACTOR = int(os.getenv("SPEEDUP_FACTOR", 60))

    # Wait for Flask server to be ready
    print("Waiting for Flask server to start...")
    time.sleep(2)  # Ensure the Flask server is ready

    generator = LogGenerator(num_logs=NUM_LOGS, timespan_minutes=TIMESPAN_MINUTES)
    logs = generator.generate_logs()

    reader = LogReader(logs, publisher, speedup_factor=SPEEDUP_FACTOR)
    print("Starting log reader...")
    reader.read_logs()

# Example Usage
if __name__ == '__main__':
    hub_name = "logger"
    publisher = Publisher(hub_name)
    publisher.connect()

    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start log reader in the main thread
    start_log_reader(publisher)