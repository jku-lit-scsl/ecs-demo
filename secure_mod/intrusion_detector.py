import logging
import time


class IDSMQTTException(Exception):
    pass


class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.call_times = []

    def update_max_calls(self, new_max_calls):
        logging.info(f'Updated MQTT msg rate to max {new_max_calls}')
        self.max_calls = new_max_calls

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            current_time = time.time()
            self.call_times.append(current_time)

            # Remove calls that are older than the period
            self.call_times = [t for t in self.call_times if current_time - t <= self.period]

            if len(self.call_times) > self.max_calls:
                logging.error('Exceeded current msg threshold')
                raise IDSMQTTException("Rate limit for MQTT exceeded.")

            return func(*args, **kwargs)

        return wrapper


# Create a RateLimiter instance
rate_limiter = RateLimiter(max_calls=999999, period=60)


@rate_limiter  # Limit to max_calls calls per minute
def rate_checker():
    pass


def set_max_calls(new_max_calls: int):
    rate_limiter.update_max_calls(new_max_calls)


def check_new_msg():
    rate_checker()
