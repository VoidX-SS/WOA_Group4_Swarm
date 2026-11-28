"""Kiểm chứng hàm chuẩn (Quadratic 1D, Sphere 30D, Rastrigin 30D) ,  lưu trữ tại Extra/benchmark/.

Chạy kiểm tra dữ liệu đã lưu: python Extra/benchmark/benchmark_suite.py --verify
Chạy lại 90 lượt benchmark:       python Extra/benchmark/benchmark_suite.py --run
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.n4_hoang_yen_du_lieu import default_settings
from src.n6_van_lam_woa import woa
from src.n7_ngoc_thanh_thuc_nghiem import save_csv, save_json
from src.n8_trang_bui_thong_ke import average, std

BENCH_DIR = Path(__file__).resolve().parent
BENCH_RESULTS = BENCH_DIR / "results"


def evaluate_benchmark(whale, problem):
    score = 0
    if problem["function"] == "quadratic":
        score = (whale[0] - 7) * (whale[0] - 7)
    elif problem["function"] == "sphere":
        for value in whale:
            score += value * value
    else:
        for value in whale:
            score += value * value - 10 * math.cos(2 * math.pi * value) + 10
    return {"score": score, "base_score": score, "valid": True, "values": whale.copy()}


def run_benchmarks(output=BENCH_RESULTS, seeds=30):
    functions = [
        {"function": "quadratic", "dimensions": 1, "lower": -20, "upper": 20, "target": 0.00000001},
        {"function": "sphere", "dimensions": 30, "lower": -100, "upper": 100, "target": 0.00000001},
        {"function": "rastrigin", "dimensions": 30, "lower": -5.12, "upper": 5.12, "target": 0.000001},
    ]
    for problem in functions:
        for seed in range(1, seeds + 1):
            settings = default_settings()
            settings["seed"] = seed
            settings["iterations"] = 500
            result = woa(evaluate_benchmark, problem, settings)
            result["final_population"] = []
            result["history"] = []
            save_json(Path(output) / "benchmarks" / problem["function"] / ("seed_" + str(seed).zfill(2) + ".json"), result)
    summarize_benchmarks(output)


def summarize_benchmarks(output=BENCH_RESULTS):
    rows = []
    for path in sorted((Path(output) / "benchmarks").glob("*/seed_*.json")):
        with open(path, encoding="utf-8") as file:
            result = json.load(file)
        problem = result["problem"]
        report = result["best_overall"]["evaluation"]
        square_distance = 0
        for value in report["values"]:
            optimum = 7 if problem["function"] == "quadratic" else 0
            square_distance += (value - optimum) ** 2
        rows.append({
            "function": problem["function"],
            "seed": result["settings"]["seed"],
            "dimensions": problem["dimensions"],
            "score": report["score"],
            "target": problem["target"],
            "success": int(report["score"] <= problem["target"]),
            "distance_to_known_optimum": math.sqrt(square_distance),
            "evaluations": result["evaluations"],
        })
    save_csv(Path(output) / "benchmark_trials.csv", rows)
    summary = []
    for name in ["quadratic", "sphere", "rastrigin"]:
        values = [r["score"] for r in rows if r["function"] == name]
        successes = sum(r["success"] for r in rows if r["function"] == name)
        if values:
            summary.append({
                "function": name,
                "n": len(values),
                "success_n": successes,
                "score_mean": average(values),
                "score_std": std(values),
            })
    save_csv(Path(output) / "benchmark_summary.csv", summary)


def verify_benchmarks(output=BENCH_RESULTS):
    count = 0
    for path in sorted((Path(output) / "benchmarks").glob("*/seed_*.json")):
        result = json.loads(path.read_text(encoding="utf-8"))
        fresh = evaluate_benchmark(result["best_overall"]["position"], result["problem"])
        assert math.isclose(fresh["score"], result["best_overall"]["evaluation"]["score"], abs_tol=1e-9)
        assert fresh["score"] <= result["problem"]["target"]
        assert result["evaluations"] == 15000
        count += 1
    assert count == 90, f"Kỳ vọng 90 JSON benchmark, tìm thấy {count}"
    print("Extra benchmark OK: 90 lượt (Quadratic 1D, Sphere 30D, Rastrigin 30D) đều đạt ngưỡng.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="Chạy lại 90 lượt benchmark.")
    parser.add_argument("--verify", action="store_true", help="Kiểm tra lại 90 lượt benchmark đã lưu.")
    args = parser.parse_args()
    if args.run:
        run_benchmarks()
    verify_benchmarks()
