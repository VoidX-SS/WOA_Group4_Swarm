"""Kiểm thử tự động cho module dữ liệu src/n4_hoang_yen_du_lieu.py."""

import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.n4_hoang_yen_du_lieu import (
    a_value,
    bounds,
    decode,
    default_settings,
    load_problem,
    validate_inputs,
)
from src.n5_quynh_ngan_buoc_woa import repair_population


class TestHoangYenData(unittest.TestCase):
    def test_01_json_problems(self):
        """Kiểm tra cả 3 bản đồ có đủ 8 trại, 3 bão, pin 220 và cổng khe [38, 62] ở Ca B."""
        for name in ["co_ban", "khe_hep", "chan_duong"]:
            prob = load_problem(name)
            self.assertEqual(prob["budget"], 220, f"{name} phải có túi pin 220")
            self.assertEqual(prob["beacon_max"], 25, f"{name} phải có pin tối đa 1 đèn = 25")
            self.assertEqual(len(prob["camps"]), 8, f"{name} phải có đúng 8 trại")
            self.assertEqual(len(prob["storms"]), 3, f"{name} phải có đúng 3 vùng bão")
            if name == "khe_hep":
                self.assertIn("gate", prob)
                self.assertEqual(prob["gate"]["x"], 40)
                self.assertEqual(prob["gate"]["y_min"], 38)
                self.assertEqual(prob["gate"]["y_max"], 62)

    def test_02_bounds_and_clipping(self):
        """Kiểm tra biên 30 biến: [0, 100] cho x/y, [0, 25] cho pin và clip biên."""
        prob = load_problem("co_ban")
        lb, ub = bounds(prob)
        self.assertEqual(len(lb), 30)
        self.assertEqual(len(ub), 30)
        for i in range(10):
            self.assertEqual(lb[3 * i], 0)
            self.assertEqual(ub[3 * i], 100)
            self.assertEqual(lb[3 * i + 1], 0)
            self.assertEqual(ub[3 * i + 1], 100)
            self.assertEqual(lb[3 * i + 2], 0)
            self.assertEqual(ub[3 * i + 2], 25)

        out_vec = [-50.0, 150.0, 99.0] * 10
        pop = [out_vec]
        repair_population(pop, lb, ub, "clip", random.Random(7))
        clipped = pop[0]
        for i in range(10):
            self.assertEqual(clipped[3 * i], 0.0)
            self.assertEqual(clipped[3 * i + 1], 100.0)
            self.assertEqual(clipped[3 * i + 2], 25.0)

    def test_03_decode_top_k_and_tie_breaking(self):
        """Kiểm tra giải mã Top-K (K=6, 8, 10): giữ đủ 10 tọa độ, tắt đèn ngoài Top-K, hòa ưu tiên chỉ số nhỏ."""
        vec = [
            10, 10, 5.0,    # 0
            20, 20, 20.0,   # 1 (hòa với 3)
            30, 30, 10.0,   # 2
            40, 40, 20.0,   # 3 (hòa với 1)
            50, 50, 15.0,   # 4 (hòa với 7)
            60, 60, 8.0,    # 5
            70, 70, 25.0,   # 6 (cao nhất)
            80, 80, 15.0,   # 7 (hòa với 4)
            90, 90, 2.0,    # 8
            95, 95, 12.0,   # 9
        ]

        prob6 = load_problem("co_ban")
        prob6["active_lights"] = 6
        beacons6 = decode(vec, prob6)
        self.assertEqual(len(beacons6), 10)
        active6 = [i for i, b in enumerate(beacons6) if b["active"]]
        disabled6 = [i for i, b in enumerate(beacons6) if not b["active"]]
        self.assertEqual(active6, [1, 3, 4, 6, 7, 9])
        self.assertEqual(disabled6, [0, 2, 5, 8])
        for idx in disabled6:
            self.assertEqual(beacons6[idx]["energy"], 0)
            self.assertEqual(beacons6[idx]["x"], vec[3 * idx])

        prob8 = load_problem("co_ban")
        prob8["active_lights"] = 8
        beacons8 = decode(vec, prob8)
        disabled8 = [i for i, b in enumerate(beacons8) if not b["active"]]
        self.assertEqual(disabled8, [0, 8])
        for idx in disabled8:
            self.assertEqual(beacons8[idx]["energy"], 0)

        prob10 = load_problem("co_ban")
        prob10["active_lights"] = 10
        beacons10 = decode(vec, prob10)
        self.assertTrue(all(b["active"] for b in beacons10))

    def test_04_a_schedules_and_validate_inputs(self):
        """Kiểm tra 3 lịch a theo t/total và kiểm tra ràng buộc đầu vào."""
        total = 600
        self.assertAlmostEqual(a_value(0, total, "linear"), 2.0)
        self.assertAlmostEqual(a_value(0, total, "cosine"), 2.0)
        self.assertAlmostEqual(a_value(0, total, "quadratic"), 2.0)

        self.assertAlmostEqual(a_value(300, total, "linear"), 1.0)
        self.assertAlmostEqual(a_value(300, total, "cosine"), 1.0)
        self.assertAlmostEqual(a_value(300, total, "quadratic"), 0.5)

        self.assertAlmostEqual(a_value(600, total, "linear"), 0.0)
        self.assertAlmostEqual(a_value(600, total, "cosine"), 0.0)
        self.assertAlmostEqual(a_value(600, total, "quadratic"), 0.0)

        prob = load_problem("co_ban")
        settings = default_settings()
        validate_inputs(prob, settings)
        with self.assertRaises(ValueError):
            a_value(0, total, "unknown")


if __name__ == "__main__":
    unittest.main()
