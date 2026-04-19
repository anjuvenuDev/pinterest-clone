from __future__ import annotations

from typing import Dict


class LLMClient:
    """Stubbed AI client to represent OpenAI/Claude integration."""

    def generate_remix(self, title: str, ingredient_swaps: Dict[str, str], goal: str = "") -> tuple[str, str]:
        swap_summary = ", ".join(f"{src}->{dst}" for src, dst in ingredient_swaps.items()) or "No swaps"
        remixed_title = f"{title} (Remix)"
        summary = f"Applied swaps: {swap_summary}. Goal: {goal or 'balanced nutrition'}"
        return remixed_title, summary
