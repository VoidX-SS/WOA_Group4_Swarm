# Phần Lưu Trữ Kiểm Chứng Benchmark (Extra/benchmark)

Thư mục này lưu trữ toàn bộ phần kiểm chuẩn nội bộ trên 3 hàm toán học chuẩn (`Quadratic`, `Sphere`, `Rastrigin`), được tách ra khỏi luồng báo cáo chính theo yêu cầu không so sánh với thuật toán ngoài trên bài toán UAV.

## Cấu hình đã chạy (`N = 30`, `T = 500`, `30 seed`)

| Hàm chuẩn | Số chiều | Miền gốc | Ngưỡng đạt | Đáp án lý thuyết | Thành công |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Quadratic** $(x - 7)^2$ | **1D** | $[-20, 20]$ | $10^{-8}$ | $x^* = 7$ | **30 / 30** |
| **Sphere** $\sum x_j^2$ | **30D** | $[-100, 100]$ | $10^{-8}$ | $\mathbf{x}^* = \mathbf{0}$ | **30 / 30** |
| **Rastrigin** | **30D** | $[-5.12, 5.12]$ | $10^{-6}$ | $\mathbf{x}^* = \mathbf{0}$ | **30 / 30** |

## Cách kiểm tra lại

```bash
python Extra/benchmark/benchmark_suite.py --verify
```
