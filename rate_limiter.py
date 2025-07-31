import time
import asyncio
from typing import Optional, List, Dict, Any
from collections import deque


class RateLimiter:
    """
    A rate limiter that limits requests to a specified number per minute.

    This class tracks request timestamps and enforces rate limits by
    delaying requests when necessary to stay within the specified limit.
    """

    def __init__(self, requests_per_minute: Optional[int] = None):
        """
        Initialize the rate limiter.

        Args:
            requests_per_minute: Maximum number of requests allowed per minute.
                                If None, no rate limiting is applied.
        """
        self.requests_per_minute = requests_per_minute
        self.request_timestamps: deque = deque()

    def _clean_old_timestamps(self):
        """Remove timestamps older than 1 minute."""
        now = time.time()
        while self.request_timestamps and now - self.request_timestamps[0] > 60:
            self.request_timestamps.popleft()

    def wait_if_needed(self):
        """
        Wait if necessary to comply with the rate limit.

        Returns:
            float: The time waited in seconds, or 0 if no wait was needed.
        """
        if not self.requests_per_minute:
            return 0  # No rate limiting

        self._clean_old_timestamps()

        # If we haven't reached the limit, no need to wait
        if len(self.request_timestamps) < self.requests_per_minute:
            self.request_timestamps.append(time.time())
            return 0

        # Calculate how long to wait
        oldest_timestamp = self.request_timestamps[0]
        now = time.time()
        time_since_oldest = now - oldest_timestamp

        # If a minute has passed since the oldest request, we can make a new request
        if time_since_oldest >= 60:
            self.request_timestamps.popleft()  # Remove the oldest
            self.request_timestamps.append(now)  # Add the current
            return 0

        # Wait until we can make a new request
        wait_time = 60 - time_since_oldest
        time.sleep(wait_time)

        # After waiting, update timestamps
        self.request_timestamps.popleft()  # Remove the oldest
        self.request_timestamps.append(time.time())  # Add the current

        return wait_time

    async def async_wait_if_needed(self):
        """
        Asynchronously wait if necessary to comply with the rate limit.

        Returns:
            float: The time waited in seconds, or 0 if no wait was needed.
        """
        if not self.requests_per_minute:
            return 0  # No rate limiting

        self._clean_old_timestamps()

        # If we haven't reached the limit, no need to wait
        if len(self.request_timestamps) < self.requests_per_minute:
            self.request_timestamps.append(time.time())
            return 0

        # Calculate how long to wait
        oldest_timestamp = self.request_timestamps[0]
        now = time.time()
        time_since_oldest = now - oldest_timestamp

        # If a minute has passed since the oldest request, we can make a new request
        if time_since_oldest >= 60:
            self.request_timestamps.popleft()  # Remove the oldest
            self.request_timestamps.append(now)  # Add the current
            return 0

        # Wait until we can make a new request
        wait_time = 60 - time_since_oldest
        await asyncio.sleep(wait_time)

        # After waiting, update timestamps
        self.request_timestamps.popleft()  # Remove the oldest
        self.request_timestamps.append(time.time())  # Add the current

        return wait_time
