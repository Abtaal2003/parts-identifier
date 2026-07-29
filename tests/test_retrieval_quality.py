"""Retrieval accuracy against the labeled query set.

Marked slow because it loads the real sentence-transformer. Run the fast
suite alone with:  pytest -m "not slow"
"""

import json
import statistics
import time
from pathlib import Path

import pytest

from retrieval import PartsIndex

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "eval" / "testcases.json").read_text(encoding="utf-8"))

# Floors, not targets. They exist to catch a regression in the embedding text,
# the catalog, or the similarity maths, not to advertise a headline number.
MIN_TOP1 = 0.85
MIN_TOP5 = 0.95
MAX_MEDIAN_LATENCY_MS = 150.0


@pytest.fixture(scope="module")
def index():
    idx = PartsIndex(ROOT / "data" / "parts_catalog.json")
    idx.build()
    return idx


@pytest.mark.slow
def test_index_covers_whole_catalog(index):
    assert index.is_ready
    assert len(index.catalog) == len(index.by_id)


@pytest.mark.slow
def test_search_before_build_raises():
    fresh = PartsIndex(ROOT / "data" / "parts_catalog.json")
    with pytest.raises(RuntimeError):
        fresh.search("anything")


@pytest.mark.slow
def test_k_is_clamped_to_catalog_size(index):
    assert len(index.search("grate", k=10_000)) == len(index.catalog)


@pytest.mark.slow
def test_scores_are_descending(index):
    scores = [r["score"] for r in index.search("cracked drainage grate", k=10)]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.slow
def test_every_testcase_references_a_real_part(index):
    by_number = {p["part_number"] for p in index.catalog}
    unknown = [c["expected_part_number"] for c in CASES
               if c["expected_part_number"] not in by_number]
    assert not unknown, f"test cases reference unknown part numbers: {unknown}"


@pytest.mark.slow
def test_retrieval_accuracy_and_latency(index):
    by_number = {p["part_number"]: p["id"] for p in index.catalog}
    top1 = top5 = 0
    latencies = []
    misses = []

    for case in CASES:
        expected_id = by_number[case["expected_part_number"]]
        t0 = time.perf_counter()
        results = index.search(case["query"], k=5)
        latencies.append((time.perf_counter() - t0) * 1000)
        ids = [r["part"]["id"] for r in results]
        if ids[0] == expected_id:
            top1 += 1
        if expected_id in ids:
            top5 += 1
        else:
            misses.append((case["query"][:60], expected_id, ids))

    n = len(CASES)
    median_ms = statistics.median(latencies)
    report = "\n".join(f"  {q!r} -> want {e}, got {g}" for q, e, g in misses)

    assert top5 / n >= MIN_TOP5, f"top-5 {top5}/{n}\n{report}"
    assert top1 / n >= MIN_TOP1, f"top-1 {top1}/{n}"
    assert median_ms <= MAX_MEDIAN_LATENCY_MS, f"median retrieval {median_ms:.1f}ms"

    print(f"\ntop-1 {top1}/{n} ({top1/n:.0%}) | "
          f"top-5 {top5}/{n} ({top5/n:.0%}) | median {median_ms:.1f}ms")
