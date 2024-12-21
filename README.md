# Logger Paradise ~ Log Gen Backend 

## Overview
Logger Paradise is a Python-based real-time logging system that generates, publishes, and subscribes to logs using Azure Web PubSub. This system is designed to simulate a log generation environment, publish logs over a WebSocket connection, and trigger alerts for warning and error logs.

## Features
- **Publisher**: Publishes logs to Azure Web PubSub.
- **Subscriber**: Listens for logs in real-time and displays alerts for `WARNING` and `ERROR` logs.
- **Log Generator**: Generates logs with `INFO`, `WARNING`, and `ERROR` levels, distributed across a configurable timespan.
- **Log Reader**: Reads generated logs and publishes them to subscribers.
- **Flask API**: Serves the Azure Web PubSub connection string to the subscriber.

---

## Installation

### Prerequisites
1. Python 3.8+ (Python 3.11 used)
2. Azure Web PubSub instance with the connection string.
3. `config.ini` file (see below for configuration details).
4. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### File Structure
```
Logger Paradise/
├── publisher.py
├── subscriber.py
├── log_generator.py
├── log_reader.py
├── launch.py
├── config.ini
└── README.md
```

---

## Configuration

### `config.ini`
Create a `config.ini` file with the following content:
```ini
[AZURE]
AZURE_STRING = <your-azure-web-pubsub-connection-string>

[SETTINGS]
NUM_LOGS = 100                # Number of logs to generate
TIMESPAN_MINUTES = 10         # Timespan for log generation (in minutes)
REAL_TIME = 60                # Duration (in seconds) over which logs will be published
```
Replace `<your-azure-web-pubsub-connection-string>` with your Azure Web PubSub connection string.

---

## Usage

### 1. Start the Application
Use the `launch.py` script to start the publisher and subscriber in separate terminal windows.

```bash
python launch.py
```

### 2. Components
- **Publisher** (`publisher.py`):
  - Runs a Flask server to provide the Web PubSub connection string.
  - Publishes generated logs to Azure Web PubSub.
- **Subscriber** (`subscriber.py`):
  - Connects to Azure Web PubSub.
  - Listens for logs in real-time.
  - Displays `INFO`, `WARNING`, and `ERROR` logs.
  - Alerts for `WARNING` (yellow) and `ERROR` (red).

---

## Scripts

### 1. `publisher.py`
Handles log generation, publishing, and serving the Azure Web PubSub connection string via a Flask API.

#### Key Functions
- `Publisher.connect()`: Connects to Azure Web PubSub.
- `Publisher.publish_log(log)`: Publishes logs as JSON to Azure Web PubSub.
- `start_flask()`: Starts the Flask server.
- `start_log_reader(publisher)`: Generates and reads logs, publishing them to Azure Web PubSub.

#### Flask API Endpoint
- `/connection-string`: Returns the Azure Web PubSub connection string.

### 2. `subscriber.py`
Subscribes to logs from Azure Web PubSub and processes them in real-time.

#### Key Functions
- `Subscriber.fetch_connection_string(api_url)`: Fetches the Web PubSub connection string from the Flask API.
- `Subscriber.subscribe()`: Listens for logs from Azure Web PubSub.
- `Subscriber.process_message(message)`: Processes received messages and triggers alerts for `WARNING` and `ERROR` logs.

### 3. `log_generator.py`
Generates logs with `INFO`, `WARNING`, and `ERROR` levels.

#### Key Classes
- `LogData`: Represents individual log data with `timestamp`, `log_type`, and `message`.
- `LogGenerator`: Generates logs across a configurable timespan.

### 4. `log_reader.py`
Reads generated logs and publishes them to Azure Web PubSub.

#### Key Functions
- `LogReader.read_logs()`: Publishes logs over a configurable duration (`REAL_TIME`).

### 5. `launch.py`
Launches the publisher and subscriber in separate terminal windows.

---

## Example Output

### Publisher
```bash
Connected to hub 'logger'.
Waiting for Flask server to start...
Starting log reader...
Sending 100 logs over 60 seconds.
Published Log: {"timestamp": "2024-12-16T13:38:19.871202Z", "log_type": "WARNING", "message": "INFO in login: Login attempted by:USER"}
```

### Subscriber
```bash
Connected to hub 'logger'. Token generated.
Connected to WebSocket.
[WARNING ALERT] 2024-12-16T13:38:19.871202Z [WARNING] INFO in login: Login attempted by:USER
[ERROR ALERT] 2024-12-16T13:38:34.871202Z [ERROR] ERROR in patient_route: Traceback (most recent call last): ...
```

---

## Customization
- Adjust settings in `config.ini`:
  - `NUM_LOGS`: Number of logs to generate.
  - `TIMESPAN_MINUTES`: Timespan for log generation.
  - `REAL_TIME`: Duration over which logs will be published.

---

## Troubleshooting
- Ensure the Azure Web PubSub connection string in `config.ini` is correct.
- Install required packages using `pip install -r requirements.txt`.
- If the Flask server or subscriber fails, verify that ports are not blocked or already in use.

---

