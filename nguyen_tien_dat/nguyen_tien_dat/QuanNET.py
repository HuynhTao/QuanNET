import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog
import json
import os

import json
import os

class KhachHang:
    def __init__(self, ma_khach, ten_khach, so_dien_thoai, tai_khoan, mat_khau, so_tien, gio_choi):
        self.ma_khach = ma_khach
        self.ten_khach = ten_khach
        self.so_dien_thoai = so_dien_thoai
        self.tai_khoan = tai_khoan
        self.mat_khau = mat_khau
        self.so_tien = so_tien
        self.gio_choi = gio_choi

    def to_dict(self):
        return {
            "ma_khach": self.ma_khach,
            "ten_khach": self.ten_khach,
            "so_dien_thoai": self.so_dien_thoai,
            "tai_khoan": self.tai_khoan,
            "mat_khau": self.mat_khau,
            "so_tien": self.so_tien,
            "gio_choi": self.gio_choi
        }

class NhanVien:
    def __init__(self, ma_nhan_vien, ten_nhan_vien, ten_dang_nhap, mat_khau, vai_tro):
        self.ma_nv = ma_nhan_vien
        self.ten_nv = ten_nhan_vien
        self.ten_dn = ten_dang_nhap
        self.mat_khau = mat_khau
        self.vai_tro = vai_tro

    def to_dict(self):
        return {
            "ma_nhan_vien": self.ma_nv,
            "ten_nhan_vien": self.ten_nv,
            "ten_dang_nhap": self.ten_dn,
            "mat_khau": self.mat_khau,
            "vai_tro": self.vai_tro
        }

class MayTinh:
    def __init__(self, ma_may, loai_may, trang_thai):
        self.ma_may = ma_may
        self.loai_may = loai_may
        self.trang_thai = trang_thai

    def to_dict(self):
        return {
            "ma_may": self.ma_may,
            "loai_may": self.loai_may,
            "trang_thai": self.trang_thai
        }

class DoAn:
    def __init__(self, ma_mon, ten_mon, gia, so_luong_ton):
        self.ma_mon = ma_mon
        self.ten_mon = ten_mon
        self.gia = gia
        self.so_luong_ton = so_luong_ton

    def to_dict(self):
        return {
            "ma_mon": self.ma_mon,
            "ten_mon": self.ten_mon,
            "gia": self.gia,
            "so_luong_ton": self.so_luong_ton
        }

class FileManager:
    def __init__(self, filename, ten_class):
        self.filename = filename
        self.ten_class = ten_class
        self.list_items = []
        self.load_data()

    def load_data(self):
        self.list_items = []
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

                if self.ten_class == "KhachHang":
                    for item in data:
                        kh = KhachHang(
                            item["ma_khach"], item["ten_khach"], item["so_dien_thoai"],
                            item["tai_khoan"], item["mat_khau"], item["so_tien"], item["gio_choi"]
                        )
                        self.list_items.append(kh)

                elif self.ten_class == "NhanVien":
                    for item in data:
                        nv = NhanVien(
                            item["ma_nhan_vien"], item["ten_nhan_vien"], item["ten_dang_nhap"],
                            item["mat_khau"], item["vai_tro"]
                        )
                        self.list_items.append(nv)

                elif self.ten_class == "MayTinh":
                    for item in data:
                        mt = MayTinh(item["ma_may"], item["loai_may"], item["trang_thai"])
                        self.list_items.append(mt)

                elif self.ten_class == "DoAn":
                    for item in data:
                        da = DoAn(item["ma_mon"], item["ten_mon"], item["gia"], item["so_luong_ton"])
                        self.list_items.append(da)
        except FileNotFoundError:
            print("Lỗi! Không tìm thấy file.")
        except Exception as e:
            print(f"Lỗi: {e}")

    def save_data(self):
        data = [item.to_dict() for item in self.list_items]
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Lỗi: {e}")

class Manager:
    def __init__(self, filename, ten_class, ma, ten):
        self.ma = ma
        self.ten = ten
        self.file = FileManager(filename, ten_class)
        self.list = self.file.list_items

    def them(self, doi_tuong):
        ma_moi = getattr(doi_tuong, self.ma)
        if self.tim_theo_ma(ma_moi):
            return False, f"Mã {ma_moi} đã tồn tại"
        
        self.list.append(doi_tuong)
        self.file.save_data()
        return True, "Thêm thành công"

    def xoa(self, ma_can_xoa):
        obj = self.tim_theo_ma(ma_can_xoa)
        if obj:
            self.list.remove(obj)
            self.file.save_data()
            return True, "Xóa thành công"
        return False, "Không tìm thấy mã"

    def sua(self, doi_tuong_moi):
        ma_can_sua = getattr(doi_tuong_moi, self.ma)
        for i, item in enumerate(self.list):
            if getattr(item, self.ma) == ma_can_sua:
                self.list[i] = doi_tuong_moi
                self.file.save_data()
                return True, "Cập nhật thành công"
        return False, "Không tìm thấy mã"

    def tim_theo_ma(self, ma_tim):
        ma_tim = str(ma_tim).strip().upper()
        for item in self.list:
            ma = str(getattr(item, self.ma)).strip().upper()
            if ma == ma_tim:
                return item
        return None

    def tim_theo_ten(self, ten_tim):
        ket_qua = []
        ten_tim = ten_tim.lower().strip()
        for item in self.list:
            ten = str(getattr(item, self.ten)).lower()
            if ten_tim in ten:
                ket_qua.append(item)
        return ket_qua

class QuanLyKhachHang(Manager):
    def __init__(self):
        super().__init__("khach_hang.json", "KhachHang", "ma_khach", "ten_khach")

class DSNV(Manager):
    def __init__(self):
        super().__init__("nhan_vien.json", "NhanVien", "ma_nv", "ten_nv")

class QuanLyMayTinh(Manager):
    def __init__(self):
        super().__init__("may_tinh.json", "MayTinh", "ma_may", "loai_may")

class QuanLyDoAn(Manager):
    def __init__(self):
        super().__init__("do_an.json", "DoAn", "ma_mon", "ten_mon")

def luu(n,ds):
    with open("n", "w", encoding="utf-8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=4)  

phien_may = {}       
def formmain(ma,vt):

    def khachhang():
        
        def capnhat(ds):
            tr.delete(*tr.get_children())
            for kh in ds:           
                tr.insert("", "end", values=(kh.ma_khach,kh.ten_khach,kh.so_dien_thoai,kh.tai_khoan,kh.so_tien,kh.gio_choi))
                
        dskh=QuanLyKhachHang()
        dskh.load_data()
        skh=tk.Toplevel() 
        skh.title("Danh sách khách hàng")
        skh.geometry("840x480")
        skh.configure(bg="#808080")

        icthem = Image.open("./img/powerbutton.png")
        icthem= icthem.resize((64, 64), Image.LANCZOS)
        icthem = ImageTk.PhotoImage(icthem)

        btn_them = tk.Button(
           skh,
           image=icthem,
           text="Mở Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
        )
        btn_them.image = icthem
        btn_them.place(x=10,y=10)

        icthem = Image.open("./img/poweron.png")
        icthem= icthem.resize((64, 64), Image.LANCZOS)
        icthem = ImageTk.PhotoImage(icthem)

        btn_them = tk.Button(
           skh,
           image=icthem,
           text="Tắt Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
        )
        btn_them.image = icthem
        btn_them.place(x=80,y=10)

        icthem = Image.open("./img/add.png")
        icthem= icthem.resize((64, 64), Image.LANCZOS)
        icthem = ImageTk.PhotoImage(icthem)

        btn_them = tk.Button(
           skh,
           image=icthem,
           text="Thêm Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
        )
        btn_them.image = icthem
        btn_them.place(x=150,y=10)

        icthem = Image.open("./img/add.png")
        icthem= icthem.resize((64, 64), Image.LANCZOS)
        icthem = ImageTk.PhotoImage(icthem)

        btn_them = tk.Button(
           skh,
           image=icthem,
           text="Thêm Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
        )
        btn_them.image = icthem
        btn_them.place(x=220,y=10)



        tr = ttk.Treeview(skh, columns=("ma_khach", "ten_khach", "so_dien_thoai", "tai_khoan","so_tien","gio_choi"), show="headings")
        tr.heading("ma_khach", text="Mã khách")
        tr.heading("ten_khach", text="Tên khách")
        tr.heading("so_dien_thoai", text="SĐT")
        tr.heading("tai_khoan", text="Tài khoản")
        tr.heading("so_tien", text="Tiền")
        tr.heading("gio_choi", text="Gời chơi còn lại")

        tr.place(x=10, y=150, width=810, height=450)

        tr.bind("<<TreeviewSelect>>")

        capnhat(dskh.list_kh)        

        skh.mainloop()

    def nhanvien():
        
        def capnhat(ds):
            tr.delete(*tr.get_children())
            for nv in ds:

                tr.insert("", "end", values=(
                    nv.get("ma_nhan_vien","Trống"),
                    nv.get("ten_nhan_vien", "Trống"),
                    nv.get("so_dien_thoai", "Trống"),
                    nv.get("vai_tro", "Trống"),
                    nv.get("ten_dang_nhap", "Trống")
                ))

        snv = tk.Toplevel() 
        snv.title("Danh sách nhân viên")
        snv.geometry("840x480")
        snv.configure(bg="#808080")

        icthem = Image.open("./img/plus.png")
        icthem = icthem.resize((64, 64), Image.LANCZOS)
        icthem = ImageTk.PhotoImage(icthem)

        btn_them = tk.Button(
            snv,
            image=icthem,
            text="Thêm NV",
            compound="top",
            bg="#808080",
            fg="white",
            bd=0,
        )
        btn_them.image = icthem
        btn_them.place(x=10, y=10)

        icsua = Image.open("./img/update.png") 
        icsua = icsua.resize((64, 64), Image.LANCZOS)
        icsua = ImageTk.PhotoImage(icsua)

        btn_sua = tk.Button(
            snv,
            image=icsua,
            text="Sửa NV",
            compound="top",
            bg="#808080",
            fg="white",
            bd=0,
        )
        btn_sua.image = icsua
        btn_sua.place(x=80, y=10)

        # Nút Xóa (Dùng tạm icon powerbutton)
        icxoa = Image.open("./img/delete.png")
        icxoa = icxoa.resize((64, 64), Image.LANCZOS)
        icxoa = ImageTk.PhotoImage(icxoa)

        btn_xoa = tk.Button(
            snv,
            image=icxoa,
            text="Xóa NV",
            compound="top",
            bg="#808080",
            fg="white",
            bd=0,
        )
        btn_xoa.image = icxoa
        btn_xoa.place(x=150, y=10)

        tr = ttk.Treeview(snv, columns=("ma_nv", "ten_nv", "sdt", "vai_tro", "tai_khoan"), show="headings")
        
        tr.heading("ma_nv", text="Mã NV")
        tr.heading("ten_nv", text="Tên nhân viên")
        tr.heading("sdt", text="SĐT")
        tr.heading("vai_tro", text="Vai trò")
        tr.heading("tai_khoan", text="Tài khoản")

        tr.column("ma_nv", width=100)
        tr.column("ten_nv", width=200)
        tr.column("sdt", width=120)
        tr.column("vai_tro", width=100)
        tr.column("tai_khoan", width=150)

        tr.place(x=10, y=150, width=810, height=450)

        tr.bind("<<TreeviewSelect>>")

        capnhat(dsnv)        

        snv.mainloop()
    def maytinh(): 
        def momay():
            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Lỗi", "Chọn máy trước")
                return

            ma_may = tr.item(chon)["values"][0]

            may = next(m for m in dsmt if m["ma_may"] == ma_may)

            if may["trang_thai"] != "trống":
                messagebox.showerror("Lỗi", "Máy đang dùng")
                return

            ma_khach = tk.simpledialog.askstring("Mở máy", "Nhập mã khách:")
            if not ma_khach:
                return

            kh = next((k for k in dskh if k["ma_khach"] == ma_khach), None)
            if not kh or kh["gio_choi"] <= 0:
                messagebox.showerror("Lỗi", "Khách không hợp lệ")
                return



            # cập nhật RAM
            phien_may[ma_may] = {
                "tai_khoan": kh["tai_khoan"],
                "gio": kh["gio_choi"],
                "ma_kh": ma_khach
            }

            may["trang_thai"] = "đang dùng"
            capnhat(dsmt)

        def tatmay_click():
            selected = tr.selection()
            if not selected:
                messagebox.showwarning("Chú ý", "Chọn máy trước khi tắt!")
                return
            ma_may = tr.item(selected[0], "values")[0]
            tatmay(ma_may)

        def tatmay(ma_may):
            if ma_may not in phien_may:
                return

            phien = phien_may.pop(ma_may)
            ma_kh = phien["ma_kh"]
            gio_con_lai = phien["gio"]

            # cộng giờ chơi cho khách
            kh = next(k for k in dskh if k["ma_khach"] == ma_kh)
            kh["gio_choi"] = kh.get("gio_choi", 0) + gio_con_lai

            # cập nhật trạng thái máy
            may = next(m for m in dsmt if m["ma_may"] == ma_may)
            may["trang_thai"] = "trống"

            # cập nhật Treeview
            capnhat(dsmt)

            messagebox.showinfo("Tắt máy", f"Máy {ma_may} đã tắt. Giờ còn lại của khách: {gio_con_lai:.2f} giờ")


        def tru_gio():
            for ma_may, phien in list(phien_may.items()):
                # trừ 1 phút
                phien["gio"] -= 1/60  

                if phien["gio"] <= 0:
                    # tìm máy
                    may = next(m for m in dsmt if m["ma_may"] == ma_may)
                    may["trang_thai"] = "trống"

                    # xóa phiên
                    phien_may.pop(ma_may)
                    tatmay(ma_may)
                    messagebox.showinfo(
                        "Hết giờ",
                        f"Máy {ma_may} đã hết giờ và tự tắt"
                    )

            capnhat(dsmt)
            smt.after(60000, tru_gio)   # gọi lại sau 60 giây


        def capnhat(ds):
            tr.delete(*tr.get_children())
            for m in ds:
                ma = m["ma_may"]
                phien = phien_may.get(ma, {})

                gio = phien.get("gio", "")
                if gio != "":
                    gio = round(gio, 2)

                tr.insert("", "end", values=(
                    ma,
                    m["loai_may"],
                    m["trang_thai"],
                    phien.get("tai_khoan", ""),
                    gio
                ))




        smt=tk.Toplevel() 
        smt.title("Danh sách máy tính")
        smt.geometry("840x480")
        smt.configure(bg="#808080")

        icthem = Image.open("./img/powerbutton.png")
        icthem= icthem.resize((64, 64), Image.LANCZOS)
        icthem = ImageTk.PhotoImage(icthem)

        btn_them = tk.Button(
           smt,
           image=icthem,
           text="Mở Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
           command=momay
        )
        btn_them.image = icthem
        btn_them.place(x=10,y=10)

        icthem = Image.open("./img/poweron.png")
        icthem= icthem.resize((64, 64), Image.LANCZOS)
        icthem = ImageTk.PhotoImage(icthem)

        btn_them = tk.Button(
           smt,
           image=icthem,
           text="Tắt Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
           command=tatmay_click
        )
        btn_them.image = icthem
        btn_them.place(x=80,y=10)

        icthem = Image.open("./img/add.png")
        icthem= icthem.resize((64, 64), Image.LANCZOS)
        icthem = ImageTk.PhotoImage(icthem)

        btn_them = tk.Button(
           smt,
           image=icthem,
           text="Thêm Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
        )
        btn_them.image = icthem
        btn_them.place(x=150,y=10)

        icthem = Image.open("./img/add.png")
        icthem= icthem.resize((64, 64), Image.LANCZOS)
        icthem = ImageTk.PhotoImage(icthem)

        btn_them = tk.Button(
           smt,
           image=icthem,
           text="Thêm Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
        )
        btn_them.image = icthem
        btn_them.place(x=220,y=10)



        tr = ttk.Treeview(smt, columns=("ma_may", "loai_may", "trang_thai", "ma_kh","thoi_gian_con_lai"), show="headings")
        tr.heading("ma_may", text="Mã máy")
        tr.heading("loai_may", text="Loại máy")
        tr.heading("trang_thai", text="Trạng thái")
        tr.heading("ma_kh", text="Tài khoản sử dụng")
        tr.heading("thoi_gian_con_lai", text="Thời gian")

        tr.place(x=10, y=150, width=810, height=450)

        tr.bind("<<TreeviewSelect>>")

        capnhat(dsmt)

        tru_gio()

        smt.mainloop()



    def dangxuat():
        s1.destroy()
        s.deiconify()
        enmk.delete(0, tk.END)

    s.withdraw()
    s1 = tk.Toplevel()
    s1.title("Quản lý quán Net")
    s1.geometry("1200x720")


    anh = Image.open("./img/anhnen3.jpg")
    anh = anh.resize((1200, 720), Image.LANCZOS)
    anhnen = ImageTk.PhotoImage(anh)


    label_nen = tk.Label(s1, image=anhnen)
    label_nen.image = anhnen
    label_nen.place(x=0, y=0, relwidth=1, relheight=1)

    icpc = Image.open("./img/desktop.png")
    icpc= icpc.resize((64, 64), Image.LANCZOS)
    icpc = ImageTk.PhotoImage(icpc)

    btn_pc = tk.Button(
        s1,
        image=icpc,
        text="Máy tính",
        compound="top",
        bg="#1e1e1e",
        fg="white",
        bd=0,
        command=maytinh
    )
    btn_pc.image = icpc 
    btn_pc.place(x=50, y=50)

    ickh = Image.open("./img/cake.png")
    ickh= ickh.resize((64, 64), Image.LANCZOS)
    ickh = ImageTk.PhotoImage(ickh)

    btn_kh = tk.Button(
        s1,
        image=ickh,
        text="Khách hàng",
        compound="top",
        bg="#1e1e1e",
        fg="white",
        bd=0,
        command=khachhang
    )
    btn_kh.image = ickh
    btn_kh.place(x=50, y=150)


    icnv = Image.open("./img/teamwork.png")
    icnv= icnv.resize((64, 64), Image.LANCZOS)
    icnv = ImageTk.PhotoImage(icnv)

    btn_nv = tk.Button(
        s1,
        image=icnv,
        text="Nhân viên",
        compound="top",
        bg="#1e1e1e",
        fg="white",
        bd=0,
        command = nhanvien
    )
    btn_nv.image = icnv
    btn_nv.place(x=50, y=250)


    icf = Image.open("./img/fast-food.png")
    icf= icf.resize((64, 64), Image.LANCZOS)
    icf = ImageTk.PhotoImage(icf)

    btn_f = tk.Button(
        s1,
        image=icf,
        text="Thức ăn",
        compound="top",
        bg="#1e1e1e",
        fg="white",
        bd=0,
        command=dangxuat
    )
    btn_f.image = icf
    btn_f.place(x=50, y=350)

    taskbar = tk.Frame(s1, bg="#2b2b2b", height=40)
    taskbar.pack(side="bottom", fill="x")

    icoff = Image.open("./img/power.png")
    icoff= icoff.resize((20, 20), Image.LANCZOS)
    icoff = ImageTk.PhotoImage(icoff)

    btn_off = tk.Button(
        taskbar,
        image=icoff,
        compound="top",
        bg="#1e1e1e",
        fg="white",
        bd=0,
        command=dangxuat
    )
    btn_off.image = icoff
    btn_off.place(x=1150, y=0)

    tk.Label(taskbar, text=f"Quán NET [{vt}]",
             fg="white", bg="#2b2b2b",
             font=("Arial", 10)).pack(side="left", padx=10)


def dangnhap():
    print(dsnv)
    ten=enten.get()
    mk=enmk.get()
    manv=None
    vt=None
    dk=False
    if ten=="" or mk=="":
        messagebox.showerror("Lỗi","Tên và Mật khẩu không để trống!!!")
        enmk.delete(0, tk.END)
    else:
        for nv in dsnv:
            if nv["ten_dang_nhap"]==ten and nv["mat_khau"]==mk:
                manv=nv["ma_nhan_vien"]
                vt=nv["vai_tro"]
                dk=True
                break
        else:
            enmk.delete(0, tk.END)
            messagebox.showerror("Lỗi","Thông tin ĐN không đúng kiểm tra lại")
        if dk:
            formmain(manv,vt)



s = tk.Tk()
s.title("Quán NET")
s.geometry("400x500")

anh = Image.open("./img/logo1.png")
anh = anh.resize((400, 500), Image.LANCZOS)
anhnen = ImageTk.PhotoImage(anh)

cvnen = tk.Canvas(s, width=640, height=320, highlightthickness=0)
cvnen.pack(fill="both", expand=True)

cvnen.create_image(0, 0, image=anhnen, anchor="nw")


cvnen.create_text(
    200, 200,
    text="ĐĂNG NHẬP",
    fill="aqua",
    font=("Arial", 14, "bold")
)

cvnen.create_text(
    130, 250,
    text="Tên đăng nhập:",
    fill="white",
    font=("Arial", 10, "bold"),
    anchor="e"
)

cvnen.create_text(
    130, 290,
    text="Mật khẩu:",
    fill="white",
    font=("Arial", 10, "bold"),
    anchor="e"
)

enten = tk.Entry(s)
cvnen.create_window(230, 250, window=enten, width=150)

enmk = tk.Entry(s, show="*")
cvnen.create_window(230, 290, window=enmk, width=150)

btn = tk.Button(s, text="ĐĂNG NHẬP", command=dangnhap)
cvnen.create_window(200, 340, window=btn, width=120, height=35)


try:
    with open("./json/do_an.json",'r',encoding="utf-8") as f:
        dsda=json.load(f)
except FileNotFoundError:
    messagebox.showerror("Lỗi", "Không tìm thấy file 1json!")

try:
    with open("./json/khach_hang.json",'r',encoding="utf-8") as f:
        dskh=json.load(f)
except FileNotFoundError:
    messagebox.showerror("Lỗi", "Không tìm thấy file 2json!")        

try:
    with open("./json/may_tinh.json",'r',encoding="utf-8") as f:
        dsmt=json.load(f)
except FileNotFoundError:
    messagebox.showerror("Lỗi", "Không tìm thấy file 3json!")

try:
    with open("./json/nhan_vien.json",'r',encoding="utf-8") as f:
        dsnv=json.load(f)
except FileNotFoundError:
    messagebox.showerror("Lỗi", "Không tìm thấy file 3json!")

s.mainloop()