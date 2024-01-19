import time

max_calls = 999999


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


def set_max_calls(new_max_calls: int):
    global max_calls
    max_calls = new_max_calls


@RateLimiter(max_calls=max_calls, period=60)  # Limit to max_calls calls per minute
def rate_checker():
    pass


def check_new_msg():
    rate_checker()
