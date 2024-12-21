from azure.messaging.webpubsubservice import WebPubSubServiceClient
from flask import Flask, jsonify
from log_generator import LogGenerator  # Assuming this is defined elsewhere
from log_reader import LogReader  # Assuming this is defined elsewhere
import threading
import time
import configparser

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

class Publisher:
    def __init__(self, hub_name):
        self.connection_string = config['AZURE'].get('AZURE_STRING')
        print(self.connection_string)
        if not self.connection_string:
            raise ValueError("AZURE_STRING is not set in config.ini under [AZURE].")
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
    connection_string = config['AZURE'].get('AZURE_STRING')
    if not connection_string:
        return jsonify({'error': 'AZURE_STRING is not set in config.ini under [AZURE]'}), 500
    return jsonify({'connection_string': connection_string})


def start_flask():
    """Start the Flask server."""
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)


def start_log_reader(publisher):
    """Generate logs and read them."""
    NUM_LOGS = int(config['SETTINGS'].get('NUM_LOGS', 100))
    TIMESPAN_MINUTES = int(config['SETTINGS'].get('TIMESPAN_MINUTES', 10))
    SPEEDUP_FACTOR = int(config['SETTINGS'].get('SPEEDUP_FACTOR', 60))

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
    flask_thread.daemon = False  # Keep Flask server running independently
    flask_thread.start()

    # Start log reader in the main thread
    start_log_reader(publisher)
