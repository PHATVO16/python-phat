import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.update_danhmuc import update_danhmuc   # <- chú ý tên file

madm = input("Nhập ID danh mục cần cập nhật: ").strip()
tendm = input("Nhập tên danh mục mới: ").strip()
mota  = input("Nhập mô tả mới: ").strip()

# (tuỳ chọn) ép kiểu ID về int nếu bảng của bạn dùng INT
# madm = int(madm)

update_danhmuc(madm, tendm, mota)
