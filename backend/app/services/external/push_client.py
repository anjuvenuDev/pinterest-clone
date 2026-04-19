from __future__ import annotations


class PushClient:
    """Stub client for Expo push notifications."""

    def send(self, user_id: str, title: str, body: str) -> dict:
        return {"sent": True, "user_id": user_id, "title": title, "body": body}
