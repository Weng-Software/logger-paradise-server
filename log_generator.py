import random
import datetime

class LogData:
    def __init__(self, timestamp, log_type, message):
        self.timestamp = timestamp
        self.log_type = log_type
        self.message = message

    def __str__(self):
        return f"{self.timestamp} {self.message}"


class LogGenerator:
    def __init__(self, num_logs=100, timespan_minutes=10):
        self.num_logs = num_logs
        self.timespan_minutes = timespan_minutes
        self.start_time = datetime.datetime.utcnow()

    def generate_logs(self):
        log_types = ["INFO", "WARNING", "ERROR"] # put into interiable
        logs = []

        for _ in range(self.num_logs):
            timestamp = self.start_time + datetime.timedelta(
                seconds=random.randint(0, self.timespan_minutes * 60)
            )
            log_type = random.choice(log_types)
            message = self._generate_message(log_type)
            logs.append(LogData(timestamp.isoformat() + "Z", log_type, message))

        return logs

    def _generate_message(self, log_type):
        if log_type == "INFO":
            return self._generate_info_message()
        elif log_type == "WARNING":
            return self._generate_warning_message()
        elif log_type == "ERROR":
            return self._generate_error_message()

    def _generate_info_message(self):
        messages = [
            "\"POST /APICALL HTTP/1.1\" 200 9426 \"-\" \"ORIGIN\"",
            "INFO in FILE: RANDOMTEXTINFO",
            "\"GET /APICALL HTTP/1.1\" 200 9426 \"-\" \"ORIGIN\"",
        ]
        return random.choice(messages)

    def _generate_warning_message(self):
        messages = [
            "INFO in login: Login attempted by:USER",
            "WARNING in FILENAME: Clinic ID blank for session: USER",
            "INFO in login: USER: PASSWORD login successful for: 123.456.78.910, 88.888.888.88:88888",
        ]
        return random.choice(messages)

    def _generate_error_message(self):
        messages = [
            "ERROR in patient_route: Traceback (most recent call last):\nFile \"FILENAME\", line 418, in FUNCTION\nERRONEOUS CODE\nFile \"FILENAME\", line 114, in FUNCTION\nERRONEOUS CODE\nAttributeError: 'REASON FOR ERROR'",
        ]
        return random.choice(messages)
