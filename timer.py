import time


class Timer():
    def __init__(self, seconds):
        self.begin_time = time.time()
        self.interval = seconds

    def check_time(self):
        return time.time() - self.begin_time >= self.interval
