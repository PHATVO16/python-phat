from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql  # Đảm bảo import đúng đường dẫn
from mysql.connector import Error

def insert_danhmuc(tendm, mota):
    """Hàm thêm danh mục mới vào bảng danhmuc."""
    try:
        # Kết nối CSDL
        connection = connect_mysql()
        if connection is None:
            print("⚠️ Không thể kết nối cơ sở dữ liệu.")
            return

        cursor = connection.cursor()

        # Câu lệnh SQL
        sql = "INSERT INTO danhmuc (tendm, mota) VALUES (%s, %s)"
        data = (tendm, mota)

        # Thực thi truy vấn
        cursor.execute(sql, data)
        connection.commit()

        print(f"✅ Đã thêm danh mục: {tendm}")

    except Error as e:
        print("❌ Lỗi khi thêm danh mục:", e)

    finally:
        # Đóng kết nối để tránh rò rỉ tài nguyên
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
