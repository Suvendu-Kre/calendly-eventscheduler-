import time
import random

def retry(func, attempts=3, delay=1, backoff=2):
    """Retry a function with exponential backoff."""
    for i in range(attempts):
        try:
            return func()
        except Exception as e:
            if i == attempts - 1:
                raise
            wait = delay * backoff ** i + random.uniform(0, 1)
            print(f"Retrying in {wait:.2f} seconds...")
            time.sleep(wait)

def circuit_breaker(func, failure_threshold=3, recovery_timeout=30):
    """A simple circuit breaker."""
    state = "CLOSED"
    failure_count = 0
    last_failure_time = None

    def wrapper(*args, **kwargs):
        nonlocal state, failure_count, last_failure_time

        if state == "OPEN":
            if time.time() - last_failure_time > recovery_timeout:
                state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN.")

        try:
            result = func(*args, **kwargs)
            failure_count = 0
            state = "CLOSED"
            return result
        except Exception as e:
            failure_count += 1
            last_failure_time = time.time()
            if failure_count >= failure_threshold:
                state = "OPEN"
                print("Circuit breaker OPEN.")
            raise
    return wrapper