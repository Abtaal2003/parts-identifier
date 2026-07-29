"""Route-level tests for /identify, /health and the static index page."""

import io

import pytest

from tests.conftest import CATALOG, JPEG, PNG, FakeCerebras


def post(client, description="cracked drainage grate", image=None):
    files = {"image": image} if image else None
    return client.post("/identify", data={"description": description}, files=files)


class TestValidation:
    def test_empty_request_rejected(self, make_client):
        r = make_client().post("/identify", data={})
        assert r.status_code == 400
        assert "photo" in r.json()["detail"].lower()

    def test_overlong_description_rejected(self, make_client):
        r = post(make_client(), description="x" * 2001)
        assert r.status_code == 400
        assert "2000" in r.json()["detail"]

    def test_description_at_limit_accepted(self, make_client):
        assert post(make_client(), description="x" * 2000).status_code == 200

    def test_declared_mime_must_be_allowed(self, make_client):
        r = post(make_client(), image=("a.gif", io.BytesIO(b"GIF89a"), "image/gif"))
        assert r.status_code == 400
        assert "image/gif" in r.json()["detail"]

    def test_spoofed_content_type_rejected_by_magic_bytes(self, make_client):
        # Claims to be a PNG, actually a Windows executable.
        r = post(make_client(), image=("x.png", io.BytesIO(b"MZ\x90\x00" * 64), "image/png"))
        assert r.status_code == 400
        assert "not a readable" in r.json()["detail"]

    def test_oversize_image_rejected(self, make_client):
        big = PNG + b"\x00" * (8 * 1024 * 1024)
        r = post(make_client(), image=("big.png", io.BytesIO(big), "image/png"))
        assert r.status_code == 400
        assert "8 MB" in r.json()["detail"]

    @pytest.mark.parametrize("raw,mime", [(PNG, "image/png"), (JPEG, "image/jpeg")])
    def test_valid_images_accepted(self, make_client, raw, mime):
        r = post(make_client(), image=(f"a.{mime[6:]}", io.BytesIO(raw), mime))
        assert r.status_code == 200


class TestHappyPath:
    def test_returns_matching_part(self, make_client):
        r = post(make_client())
        assert r.status_code == 200
        body = r.json()
        assert body["match"] is True
        assert body["part"]["id"] == CATALOG[0]["id"]
        assert body["confidence"] == "high"

    def test_response_shape_is_complete(self, make_client):
        body = post(make_client()).json()
        assert set(body) == {
            "match", "part", "confidence", "asset_identified",
            "damage_summary", "reasoning", "message", "candidates", "timings",
        }
        assert set(body["timings"]) == {
            "caption_ms", "retrieval_ms", "identify_ms", "total_ms"
        }
        assert len(body["candidates"]) == 5
        assert set(body["candidates"][0]) == {"id", "part_name", "score"}

    def test_part_is_fully_typed(self, make_client):
        part = post(make_client()).json()["part"]
        assert set(part) == set(CATALOG[0])
        assert isinstance(part["unit_price_usd"], float)
        assert isinstance(part["in_stock"], int)
        assert isinstance(part["keywords"], list)

    def test_text_only_request_skips_captioning(self, make_client):
        fake = FakeCerebras()
        body = post(make_client(fake)).json()
        assert len(fake.calls) == 1  # identify only, no caption call
        assert body["timings"]["caption_ms"] == 0

    def test_image_request_captions_first(self, make_client):
        fake = FakeCerebras()
        client = make_client(fake)
        post(client, image=("a.png", io.BytesIO(PNG), "image/png"))
        assert len(fake.calls) == 2  # caption, then identify


class TestGuards:
    """The security-relevant behaviour: the model cannot invent a part."""

    def test_hallucinated_part_id_is_rejected(self, make_client):
        fake = FakeCerebras(reply={"match": True, "part_id": "TOTALLY-MADE-UP",
                                   "confidence": "high", "asset_identified": "Grate",
                                   "damage_summary": "", "reasoning": "", "message": ""})
        body = post(make_client(fake)).json()
        assert body["match"] is False
        assert body["part"] is None
        assert "special order" in body["message"]

    def test_real_part_outside_the_shortlist_is_rejected(self, make_client):
        # A genuine catalog ID that retrieval did not surface must still fail.
        outsider = CATALOG[50]["id"]
        fake = FakeCerebras(reply={"match": True, "part_id": outsider,
                                   "confidence": "high", "asset_identified": "",
                                   "damage_summary": "", "reasoning": "", "message": ""})
        body = post(make_client(fake)).json()
        assert body["match"] is False
        assert body["part"] is None

    def test_no_match_response_passes_through(self, make_client):
        fake = FakeCerebras(reply={"match": False, "part_id": None, "confidence": "low",
                                   "asset_identified": "A cat", "damage_summary": "",
                                   "reasoning": "Not infrastructure.",
                                   "message": "That looks like a cat."})
        body = post(make_client(fake)).json()
        assert body["match"] is False
        assert body["part"] is None
        assert body["asset_identified"] == "A cat"


class TestErrorMapping:
    def test_unreadable_model_output_is_502(self, make_client):
        fake = FakeCerebras(raises=ValueError("no json"))
        r = post(make_client(fake))
        assert r.status_code == 502
        assert "unreadable" in r.json()["detail"]

    def test_timeout_is_504(self, make_client):
        fake = FakeCerebras(raises=RuntimeError("request timed out after 45s"))
        r = post(make_client(fake))
        assert r.status_code == 504

    def test_other_sdk_failure_is_502(self, make_client):
        fake = FakeCerebras(raises=RuntimeError("connection reset"))
        assert post(make_client(fake)).status_code == 502

    def test_missing_api_key_is_500(self, make_client, monkeypatch):
        import app as app_module

        client = make_client()
        monkeypatch.setattr(app_module, "_client", None)
        r = post(client)
        assert r.status_code == 500
        assert "CEREBRAS_API_KEY" in r.json()["detail"]


class TestMeta:
    def test_health(self, make_client):
        body = make_client().get("/health").json()
        assert body["status"] == "ok"
        assert body["parts"] == len(CATALOG)
        assert "index_ready" in body

    def test_index_page_served(self, make_client):
        r = make_client().get("/")
        assert r.status_code == 200
        assert b"<html" in r.content.lower()

    def test_openapi_documents_part_schema(self, make_client):
        schema = make_client().get("/openapi.json").json()
        assert "Part" in schema["components"]["schemas"]
        assert "IdentifyResponse" in schema["components"]["schemas"]
