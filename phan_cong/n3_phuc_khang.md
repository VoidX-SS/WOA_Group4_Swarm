# Phúc Khang

Mở [src/n3_phuc_khang_danh_gia.py](../../src/n3_phuc_khang_danh_gia.py) và dùng bảng dưới để đối chiếu.

| Bước | Nội dung làm | Đầu vào | Đầu ra |
|---|---|---|---|
| 1 | Ghép phiếu chấm | Hình học của Tuấn, pin/utility của Phong | Base, penalty, J và valid độc lập |
| 2 | Kiểm cổng khe | Các đoạn và x=40,y=38..62 | Through_gate chỉ true khi toàn đường hợp lệ |
| 3 | Kiểm chuẩn phụ (Extra) | Chuyển sang `Extra/benchmark/` | 90 lượt tách riêng khỏi luồng bài toán UAV |
| 4 | Chấm lại dữ liệu | Các position đã lưu trong ba sổ | Score/valid tái tính khớp và hình học được kiểm độc lập |

Bạn chọn một hàm nhỏ trong phần mình, lần từ đầu vào đến return, rồi chỉ một kết quả thật. Không cần thuộc mười module một lượt. Tên trên file là trách nhiệm theo phân công; nhóm thực hiện PR và review thật để ghi nhận đóng góp.
