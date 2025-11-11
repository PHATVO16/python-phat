import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.insertdanhmuc import insert_danhmuc


while True:
    ten = input("Nhập vào tên danh mục: ")
    mota = input("Nhập vào mô tả: ")

    # Gọi hàm thêm danh mục
    insert_danhmuc(ten, mota)

    # Hỏi người dùng có muốn tiếp tục không
    con = input("👉 Tiếp tục thêm (nhấn y hoặc Y), thoát thì nhấn phím bất kỳ: ")

    if con.lower() != "y":  # dùng .lower() để nhận cả y hoặc Y
        print("🛑 Kết thúc chương trình thêm danh mục.")
        break
