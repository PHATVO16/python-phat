import sys, os
# Thêm đường dẫn cha để Python tìm được thư mục common/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.delete_danhmuc import delete_danhmuc

# Nhập mã danh mục cần xóa
ma = input("Nhập vào mã danh mục cần xóa: ")

# Gọi hàm xóa
delete_danhmuc(ma)
