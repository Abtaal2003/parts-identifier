"""Unit tests for the pure helpers in app.py."""

import pytest

from app import extract_json, sniff_mime
from tests.conftest import JPEG, PNG, WEBP


class TestExtractJson:
    def test_bare_object(self):
        assert extract_json('{"match": true}') == {"match": True}

    def test_fenced_object(self):
        assert extract_json('```json\n{"match": false}\n```') == {"match": False}

    def test_object_with_surrounding_prose(self):
        assert extract_json('Sure! {"a": 1} Hope that helps.') == {"a": 1}

    def test_no_object_raises_value_error(self):
        with pytest.raises(ValueError):
            extract_json("I could not decide.")

    def test_malformed_json_raises_value_error(self):
        # json.JSONDecodeError subclasses ValueError, which is what the route
        # catches to return a 502.
        with pytest.raises(ValueError):
            extract_json('{"match": tru}')


class TestSniffMime:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            (PNG, "image/png"),
            (JPEG, "image/jpeg"),
            (WEBP, "image/webp"),
            (b"GIF89a" + b"\x00" * 32, None),
            (b"MZ\x90\x00 windows executable", None),
            (b"", None),
            (b"\x89PNG", None),  # truncated signature
        ],
    )
    def test_detects_real_type(self, raw, expected):
        assert sniff_mime(raw) == expected

    def test_riff_that_is_not_webp_is_rejected(self):
        assert sniff_mime(b"RIFF\x00\x00\x00\x00WAVE" + b"\x00" * 32) is None
