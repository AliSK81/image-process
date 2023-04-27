import datetime
import sys
import threading


class Logger:
    def __init__(self, filename):
        self.filename = filename

    def log(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        thread_id = threading.get_ident()
        log_message = f'[{timestamp}] [Thread-{thread_id}] {message}'
        with open(self.filename, 'a') as f:
            f.write(log_message + '\n')
        print(log_message, file=sys.stdout)
