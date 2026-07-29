"""Shared fixtures.

The fast suite never touches the network and never loads torch: the Cerebras
client and the retrieval step are both replaced with fakes, so these tests
exercise the routing, validation and guard logic in isolation.
"""

import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as app_module  # noqa: E402

CATALOG = json.loads(
    (Path(__file__).resolve().parents[1] / "data" / "parts_catalog.json").read_text(
        encoding="utf-8"
    )
)
SHORTLIST = [{"part": p, "score": 0.9 - i * 0.05} for i, p in enumerate(CATALOG[:5])]

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 128
JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 128
WEBP = b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 128


class FakeCerebras:
    """Stands in for the SDK client. `reply` is what the identify call returns."""

    def __init__(self, reply=None, raises=None):
        self.reply = reply if reply is not None else {
            "match": True,
            "part_id": CATALOG[0]["id"],
            "confidence": "high",
            "asset_identified": "Traffic light",
            "damage_summary": "Red lamp is dead.",
            "reasoning": "Matches the 200mm red module.",
            "message": "Order the red LED module.",
        }
        self.raises = raises
        self.calls = []
        self.chat = self

    @property
    def completions(self):
        return self

    def create(self, model, max_tokens, temperature, messages):
        self.calls.append(messages)
        if self.raises is not None:
            raise self.raises
        is_caption = "You describe photos" in messages[0]["content"]
        text = (
            "A 200mm traffic signal head with a dead red lamp."
            if is_caption
            else json.dumps(self.reply)
        )
        return type(
            "R", (), {"choices": [type("C", (), {"message": type("M", (), {"content": text})()})()]}
        )()


@pytest.fixture
def make_client(monkeypatch):
    """Build a TestClient with the model call and retrieval step faked out.

    TestClient is used without a context manager on purpose: that skips the
    lifespan handler, so no embedding model is downloaded or loaded.
    """

    def _make(fake=None, shortlist=SHORTLIST):
        monkeypatch.setattr(app_module, "_client", fake if fake else FakeCerebras())
        monkeypatch.setattr(app_module.index, "search", lambda q, k=5: shortlist)
        return TestClient(app_module.app)

    return _make
