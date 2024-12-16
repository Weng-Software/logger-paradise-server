import datetime, time
from dotenv import load_dotenv
import os
# Add constants in .env for num_logs, timespan_minutes and speedup_factor
class LogReader:
    SPEEDUP_FACTOR = int(os.getenv("SPEEDUP_FACTOR", 60))
    def __init__(self, logs, publisher, speedup_factor=SPEEDUP_FACTOR):
        """
        The speedup factor determines how much faster logs are read compared to real-time.
        A speedup_factor of 60 means that logs spanning 1 minute of real time will be processed in 1 second.
        """
        self.logs = sorted(logs, key=lambda x: x.timestamp)
        self.publisher = publisher
        self.speedup_factor = speedup_factor

    def read_logs(self):
        """Distribute logs evenly across the speedup factor duration."""
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
            print(f"Processed Log: {log}") 
            # find out when the traceback happens
            # JSON class is to be sent to the sub
