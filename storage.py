"""Persistência local em um único arquivo JSON."""

from __future__ import annotations

import json
from pathlib import Path


class JsonStorage:
    def __init__(self, path: str | Path = "data.json") -> None:
        self.path = Path(path)

    def load(self) -> dict:
        if not self.path.exists():
            return {"clinic": None, "appointments": []}

        with self.path.open(encoding="utf-8") as file:
            return json.load(file)

    def save(self, data: dict) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
