import datetime, time

class LogReader:
    def __init__(self, logs, publisher, speedup_factor=60):
        self.logs = sorted(logs, key=lambda x: x.timestamp)
        self.publisher = publisher
        self.speedup_factor = speedup_factor

    def read_logs(self):
        if not self.logs:
            print("No logs to read.")
            return

        start_time = datetime.datetime.fromisoformat(self.logs[0].timestamp[:-1])
        for log in self.logs:
            current_time = datetime.datetime.fromisoformat(log.timestamp[:-1])
            elapsed_real_time = (current_time - start_time).total_seconds() / self.speedup_factor
            time.sleep(elapsed_real_time)
            self.publisher.publish_log(log)
