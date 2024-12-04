import datetime, time

class LogReader:
    def __init__(self, logs, publisher, speedup_factor=60): # comments on how speed up works
        self.logs = sorted(logs, key=lambda x: x.timestamp)
        self.publisher = publisher
        self.speedup_factor = speedup_factor

    def read_logs(self):
        if not self.logs:
            print("No logs to read.")
            return

        total_duration = self.speedup_factor
        # Time interval between logs
        interval = total_duration / len(self.logs)

        print(f"Sending {len(self.logs)} logs over {total_duration} seconds.")
        for log in self.logs:
            self.publisher.publish_log(log)
            time.sleep(interval)
            # find out when the traceback happens
            # JSON class is to be sent to the sub
