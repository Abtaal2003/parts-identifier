"""Local retrieval layer for the parts catalog (no external services).

Embeds every catalog entry with a sentence-transformer (runs on CPU,
downloads once from Hugging Face on first run, ~80MB) and answers
top-k queries via cosine similarity in NumPy. Embeddings are cached in
data/cache/ keyed by a hash of the catalog, so restarts are instant.
"""

import hashlib
import json
import time
from pathlib import Path

import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DATA_DIR = Path(__file__).parent / "data"
CACHE_DIR = DATA_DIR / "cache"


def _part_text(p: dict) -> str:
    return (
        f"{p['asset_type']}. {p['part_name']}. {p['description']} "
        f"Keywords: {', '.join(p['keywords'])}"
    )


class PartsIndex:
    def __init__(self, catalog_path: Path):
        self.catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        self.by_id = {p["id"]: p for p in self.catalog}
        self._model = None
        self._embeddings = None
        self._catalog_hash = hashlib.md5(
            catalog_path.read_bytes()
        ).hexdigest()[:12]

    @property
    def model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(MODEL_NAME)
        return self._model

    def build(self) -> float:
        """Load cached embeddings or compute them. Returns build seconds."""
        t0 = time.perf_counter()
        CACHE_DIR.mkdir(exist_ok=True)
        cache_file = CACHE_DIR / f"embeddings-{self._catalog_hash}.npy"
        if cache_file.exists():
            self._embeddings = np.load(cache_file)
        else:
            texts = [_part_text(p) for p in self.catalog]
            emb = self.model.encode(
                texts, normalize_embeddings=True, show_progress_bar=False
            )
            self._embeddings = np.asarray(emb, dtype=np.float32)
            np.save(cache_file, self._embeddings)
        return time.perf_counter() - t0

    def search(self, query: str, k: int = 5) -> list[dict]:
        """Return top-k parts with cosine similarity scores."""
        q = self.model.encode([query], normalize_embeddings=True)[0]
        sims = self._embeddings @ q  # cosine (vectors are normalized)
        top = np.argsort(-sims)[:k]
        return [
            {"part": self.catalog[i], "score": round(float(sims[i]), 4)}
            for i in top
        ]
