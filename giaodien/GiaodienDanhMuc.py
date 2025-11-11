import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# ===== CẤU HÌNH DB: sửa cho đúng của bạn =====
DB = {
    "host": "localhost",
    "user": "root",
    "password": "",            # nếu XAMPP thường để trống
    "database": "qlthuocankhang"  # ĐỔI thành DB của bạn
}
TABLE = "danhmuc"

class DanhMucApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý Danh mục (MaDM, TenDM, MoTa)")
        self.geometry("860x480")
        self.resizable(False, False)
        self.selected_id = None

        self._build_form()
        self._build_table()
        self.load_data()

    # ---------- DB ----------
    def conn(self):
        try:
            return mysql.connector.connect(**DB)
        except Error as e:
            messagebox.showerror("Lỗi kết nối MySQL", str(e))
            return None

    # ---------- UI ----------
    def _build_form(self):
        box = ttk.LabelFrame(self, text="Thông tin danh mục")
        box.place(x=10, y=10, width=840, height=150)

        ttk.Label(box, text="MaDM (auto):").grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.v_id = tk.StringVar()
        ttk.Entry(box, textvariable=self.v_id, state="readonly", width=16)\
            .grid(row=0, column=1, padx=8, pady=6, sticky="w")

        ttk.Label(box, text="TenDM:").grid(row=1, column=0, padx=8, pady=6, sticky="w")
        self.v_name = tk.StringVar()
        ttk.Entry(box, textvariable=self.v_name, width=40)\
            .grid(row=1, column=1, padx=8, pady=6, sticky="w")

        ttk.Label(box, text="MoTa:").grid(row=0, column=2, padx=8, pady=6, sticky="w")
        self.t_desc = tk.Text(box, width=45, height=4)
        self.t_desc.grid(row=0, column=3, rowspan=2, padx=8, pady=6, sticky="w")

        btns = ttk.Frame(box); btns.grid(row=2, column=0, columnspan=4, pady=4, sticky="w")
        ttk.Button(btns, text="Thêm",     command=self.add).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Cập nhật", command=self.update).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Xóa",      command=self.delete).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text="Làm mới",  command=self.clear).grid(row=0, column=3, padx=4)
        ttk.Button(btns, text="Tải lại",  command=self.load_data).grid(row=0, column=4, padx=4)

    def _build_table(self):
        frame = ttk.LabelFrame(self, text="Danh sách (MaDM, TenDM, MoTa)")
        frame.place(x=10, y=170, width=840, height=300)

        self.tree = ttk.Treeview(frame, columns=("MaDM", "TenDM", "MoTa"), show="headings", height=11)
        self.tree.heading("MaDM", text="MaDM")
        self.tree.heading("TenDM", text="TenDM")
        self.tree.heading("MoTa",  text="MoTa")

        self.tree.column("MaDM", width=80, anchor="center")
        self.tree.column("TenDM", width=220, anchor="w")
        self.tree.column("MoTa",  width=520, anchor="w")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # ---------- CRUD ----------
    def load_data(self):
        cn = self.conn()
        if not cn: return
        try:
            cur = cn.cursor()
            cur.execute(f"SELECT MaDM, TenDM, COALESCE(MoTa,'') FROM `{DB['database']}`.`{TABLE}` ORDER BY MaDM ASC")
            rows = cur.fetchall()
            for i in self.tree.get_children():
                self.tree.delete(i)
            for r in rows:
                self.tree.insert("", "end", values=r)
        except Error as e:
            messagebox.showerror("Lỗi tải dữ liệu", str(e))
        finally:
            cur.close(); cn.close()

    def add(self):
        name = self.v_name.get().strip()
        mota = self.t_desc.get("1.0", "end").strip()
        if not name:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập TenDM.")
            return
        cn = self.conn()
        if not cn: return
        try:
            cur = cn.cursor()
            cur.execute(f"INSERT INTO `{TABLE}` (TenDM, MoTa) VALUES (%s, %s)",
                        (name, mota if mota else None))
            cn.commit()
            messagebox.showinfo("OK", "Đã thêm danh mục.")
            self.clear(); self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi thêm", str(e))
        finally:
            cur.close(); cn.close()

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Chưa chọn", "Chọn 1 dòng để cập nhật.")
            return
        name = self.v_name.get().strip()
        mota = self.t_desc.get("1.0", "end").strip()
        if not name:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập TenDM.")
            return
        cn = self.conn()
        if not cn: return
        try:
            cur = cn.cursor()
            cur.execute(f"UPDATE `{TABLE}` SET TenDM=%s, MoTa=%s WHERE MaDM=%s",
                        (name, mota if mota else None, self.selected_id))
            cn.commit()
            messagebox.showinfo("OK", f"Đã cập nhật MaDM={self.selected_id}.")
            self.clear(); self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi cập nhật", str(e))
        finally:
            cur.close(); cn.close()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Chưa chọn", "Chọn 1 dòng để xóa.")
            return
        if not messagebox.askyesno("Xác nhận", f"Xóa MaDM={self.selected_id}?"):
            return
        cn = self.conn()
        if not cn: return
        try:
            cur = cn.cursor()
            cur.execute(f"DELETE FROM `{TABLE}` WHERE MaDM=%s", (self.selected_id,))
            cn.commit()
            messagebox.showinfo("OK", f"Đã xóa MaDM={self.selected_id}.")
            self.clear(); self.load_data()
        except Error as e:
            messagebox.showerror("Lỗi xóa", str(e))
        finally:
            cur.close(); cn.close()

    # ---------- Helpers ----------
    def on_select(self, _):
        sel = self.tree.selection()
        if not sel: return
        madm, tendm, mota = self.tree.item(sel[0], "values")
        self.selected_id = madm
        self.v_id.set(madm)
        self.v_name.set(tendm)
        self.t_desc.delete("1.0", "end")
        self.t_desc.insert("1.0", mota)

    def clear(self):
        self.selected_id = None
        self.v_id.set("")
        self.v_name.set("")
        self.t_desc.delete("1.0", "end")

if __name__ == "__main__":
    DanhMucApp().mainloop()
