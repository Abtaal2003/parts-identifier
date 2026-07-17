"""Evaluation harness for the local retrieval index.

Measures retrieval quality of the local RAG index over 50 labeled test
queries (no API key or cost needed):

    uv run python eval/run_eval.py

Reports top-1 / top-3 / top-5 retrieval accuracy and median retrieval
latency. With --full it additionally runs the end-to-end pipeline through
the Cerebras API (text-only) and reports final identification accuracy
(requires CEREBRAS_API_KEY in .env; ~50 small API calls).
"""

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from retrieval import PartsIndex  # noqa: E402

CASES_PATH = Path(__file__).parent / "testcases.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="also run end-to-end API eval")
    args = ap.parse_args()

    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    index = PartsIndex(ROOT / "data" / "parts_catalog.json")
    build_s = index.build()

    by_number = {p["part_number"]: p["id"] for p in index.catalog}
    missing = [c["expected_part_number"] for c in cases
               if c["expected_part_number"] not in by_number]
    if missing:
        raise SystemExit(f"Test cases reference unknown part numbers: {missing}")

    top1 = top3 = top5 = 0
    latencies = []
    failures = []
    for c in cases:
        expected_id = by_number[c["expected_part_number"]]
        t0 = time.perf_counter()
        results = index.search(c["query"], k=5)
        latencies.append((time.perf_counter() - t0) * 1000)
        ids = [r["part"]["id"] for r in results]
        if ids[0] == expected_id:
            top1 += 1
        if expected_id in ids[:3]:
            top3 += 1
        if expected_id in ids[:5]:
            top5 += 1
        else:
            failures.append((c["query"], c["expected_part_number"], ids))

    n = len(cases)
    print(f"\n=== Retrieval evaluation ({n} test queries, "
          f"{len(index.catalog)}-part catalog) ===")
    print(f"Index build/load time : {build_s:.2f}s")
    print(f"Top-1 accuracy        : {top1}/{n}  ({100*top1/n:.1f}%)")
    print(f"Top-3 accuracy        : {top3}/{n}  ({100*top3/n:.1f}%)")
    print(f"Top-5 accuracy        : {top5}/{n}  ({100*top5/n:.1f}%)")
    print(f"Median retrieval time : {statistics.median(latencies):.1f} ms")

    if failures:
        print(f"\nMisses outside top-5 ({len(failures)}):")
        for q, exp, got in failures:
            print(f"  '{q}' -> expected {exp}, got {got}")

    if args.full:
        run_full(cases, index, by_number)


def run_full(cases, index, by_number):
    """End-to-end: retrieval + Cerebras identification (text-only)."""
    import os

    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    if not os.environ.get("CEREBRAS_API_KEY"):
        raise SystemExit("--full needs CEREBRAS_API_KEY in .env")

    from cerebras.cloud.sdk import Cerebras

    from app import extract_json, identify_from_candidates

    client = Cerebras(api_key=os.environ["CEREBRAS_API_KEY"],
                      timeout=45.0, max_retries=2)
    correct = 0
    e2e_latencies = []
    for i, c in enumerate(cases, 1):
        expected_id = by_number[c["expected_part_number"]]
        t0 = time.perf_counter()
        candidates = index.search(c["query"], k=5)
        try:
            result = identify_from_candidates(client, candidates, c["query"], "", None)
        except Exception as e:
            print(f"  [{i}/{len(cases)}] API error: {e}")
            continue
        e2e_latencies.append((time.perf_counter() - t0) * 1000)
        if result.get("part_id") == expected_id:
            correct += 1
        print(f"  [{i}/{len(cases)}] {'OK ' if result.get('part_id') == expected_id else 'MISS'}"
              f" expected {expected_id}, got {result.get('part_id')}")

    n = len(e2e_latencies)
    if n:
        print(f"\n=== End-to-end evaluation (retrieval + LLM identification) ===")
        print(f"Final accuracy     : {correct}/{n}  ({100*correct/n:.1f}%)")
        print(f"Median E2E latency : {statistics.median(e2e_latencies):.0f} ms")


if __name__ == "__main__":
    main()
