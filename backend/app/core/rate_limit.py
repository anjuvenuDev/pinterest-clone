from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Deque, Dict


class RateLimiter:
    def __init__(self, requests_per_minute: int = 120) -> None:
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        self.hits: Dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, client_ip: str) -> bool:
        now = time.time()
        bucket = self.hits[client_ip]

        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()

        if len(bucket) >= self.requests_per_minute:
            return False

        bucket.append(now)
        return True
