import time
import configparser

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

class LogReader:
    REAL_TIME = int(config['SETTINGS'].get('SPEEDUP_FACTOR', 60))
    def __init__(self, logs, publisher, speedup_factor=REAL_TIME):
        """
        The REAL_TIME here allows yout to determines how much faster logs are read/published in real-time.
        A REAL_TIME of 60 means it will take 60 seconds for the NUM_LOGS to be published.
        """
        self.logs = sorted(logs, key=lambda x: x.timestamp)
        self.publisher = publisher
        self.speedup_factor = speedup_factor

    def read_logs(self):
        """Distribute logs evenly across the REAL_TIME duration."""
        if not self.logs:
            print("No logs to read.")
            return

        # Total duration for logs to be sent
        total_duration = self.speedup_factor
        # Interval between log publications
        interval = total_duration / len(self.logs)

        print(f"Sending {len(self.logs)} logs over {total_duration} seconds.")
        for log in self.logs:
            self.publisher.publish_log(log)
            time.sleep(interval)
