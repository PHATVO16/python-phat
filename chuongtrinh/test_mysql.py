import sys
import os

# Thêm đường dẫn cha (DB_PHAT) vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Bây giờ có thể import từ ketnoidb được
from ketnoidb.ketnoi_mysql import connect_mysql

connect_mysql()
