from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List


class WorkerBus:
    """
    Lightweight async-compatible worker bus.
    We keep explicit queues for architectural clarity while processing jobs
    immediately in this scaffold for deterministic tests.
    """

    def __init__(self) -> None:
        self.queue_names = ["search_indexing", "scraper_jobs", "feed_ranking"]
        self._pending: Dict[str, List[dict]] = {name: [] for name in self.queue_names}
        self.processed_counts: Dict[str, int] = defaultdict(int)
        self._running = False

    async def start(self) -> None:
        self._running = True

    async def stop(self) -> None:
        self._running = False

    async def enqueue(self, queue_name: str, payload: dict) -> None:
        if queue_name not in self._pending:
            raise ValueError(f"Unknown queue: {queue_name}")
        self._pending[queue_name].append(payload)
        self._process_next(queue_name)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "running": self._running,
            "queue_sizes": {name: len(self._pending[name]) for name in self.queue_names},
            "processed": dict(self.processed_counts),
        }

    def _process_next(self, queue_name: str) -> None:
        if not self._pending[queue_name]:
            return
        self._pending[queue_name].pop(0)
        self.processed_counts[queue_name] += 1
