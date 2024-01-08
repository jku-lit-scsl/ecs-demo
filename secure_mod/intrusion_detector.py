import time


class IDSMQTTException(Exception):
    pass


class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.call_times = []

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            current_time = time.time()
            self.call_times.append(current_time)

            # Remove calls that are older than the period
            self.call_times = [t for t in self.call_times if current_time - t <= self.period]

            if len(self.call_times) > self.max_calls:
                raise IDSMQTTException("Rate limit for MQTT exceeded.")

            return func(*args, **kwargs)

        return wrapper


@RateLimiter(max_calls=100, period=10)  # Limit to 100 calls per 10 seconds
def rate_checker():
    pass


def check_new_msg():
    rate_checker()
