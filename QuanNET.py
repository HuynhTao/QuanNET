import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog
import json
import os
import datetime
import re

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
    def __init__(self, ma_nhan_vien, ten_nhan_vien, so_dien_thoai, ten_dang_nhap, mat_khau, vai_tro,luong):
        self.ma_nhan_vien = ma_nhan_vien
        self.ten_nhan_vien = ten_nhan_vien
        self.so_dien_thoai = so_dien_thoai
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = mat_khau
        self.vai_tro = vai_tro
        self.luong=luong
        

    def to_dict(self):
        return {
            "ma_nhan_vien": self.ma_nhan_vien,
            "ten_nhan_vien": self.ten_nhan_vien,
            "so_dien_thoai": self.so_dien_thoai,
            "ten_dang_nhap": self.ten_dang_nhap,
            "mat_khau": self.mat_khau,
            "vai_tro": self.vai_tro,
            "luong": self.luong
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

class DichVu:
    def __init__(self, ma_dd, ten_dd, gia, loai,so_luong_ton):
        self.ma_dd = ma_dd
        self.ten_dd = ten_dd
        self.gia = gia
        self.loai = loai
        self.so_luong_ton = so_luong_ton

    def to_dict(self):
        return {
            "ma_dd": self.ma_dd,
            "ten_dd": self.ten_dd,
            "gia": self.gia,
            "loai": self.loai,
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
            print(self.filename)
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
                            item["ma_nhan_vien"], item["ten_nhan_vien"],item["so_dien_thoai"],
                            item["ten_dang_nhap"],item["mat_khau"], item["vai_tro"],item["luong"])
                        self.list_items.append(nv)

                elif self.ten_class == "MayTinh":
                    for item in data:
                        mt = MayTinh(item["ma_may"], item["loai_may"], item["trang_thai"])
                        self.list_items.append(mt)

                elif self.ten_class == "DichVu":
                    for item in data:
                        DV = DichVu(item["ma_dd"], item["ten_dd"], item["gia"], item["loai"], item["so_luong_ton"])
                        self.list_items.append(DV)
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
    
    def sap_xep_ma_tang(self):
        def extract_number(item):
            ma_val = str(getattr(item, self.ma))
            numbers = re.findall(r'\d+', ma_val)
            return int(numbers[0]) if numbers else 0

        self.list.sort(key=extract_number)
class DSKH(Manager):
    def __init__(self):
        super().__init__("./json/khach_hang.json", "KhachHang", "ma_khach", "ten_khach")

class DSNV(Manager):
    def __init__(self):
        super().__init__("./json/nhan_vien.json", "NhanVien", "ma_nhan_vien", "ten_nhan_vien")

class DSMT(Manager):
    def __init__(self):
        super().__init__("./json/may_tinh.json", "MayTinh", "ma_may", "loai_may")

class DSDV(Manager):
    def __init__(self):
        super().__init__("./json/dich_vu.json", "DichVu", "ma_dd", "ten_dd")

def luu(n,ds):
    with open("n", "w", encoding="utf-8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=4)  

     
def formmain(ma,vt):
    dsmt=DSMT()
    dskh=DSKH()
    dsnv=DSNV()
    dsdv=DSDV()
    phien_may = {}  
    
    def khachhang():
        
        
        def naptienKH():
            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Thông báo", "Vui lòng chọn khách hàng cần nạp tiền!")
                return
        
            item_data = tr.item(chon)['values']
            ma_kh = item_data[0]
            ten_kh = item_data[1]
        
            f_nap = tk.Toplevel(skh)
            f_nap.title("Nạp tiền tài khoản")
            f_nap.geometry("350x250")
            f_nap.resizable(False, False)
            f_nap.grab_set() 
        
            tk.Label(f_nap, text=f"NẠP TIỀN KHÁCH HÀNG", font=("Arial", 11, "bold")).pack(pady=10)
            tk.Label(f_nap, text=f"Khách hàng: {ten_kh}", fg="blue").pack()
            
            tk.Label(f_nap, text="Nhập số tiền nạp (VNĐ):", pady=5).pack()
            ent_so_tien = tk.Entry(f_nap, font=("Arial", 12), justify="center")
            ent_so_tien.pack(pady=5, padx=30, fill="x")
            ent_so_tien.focus_set()
        
            def xac_nhan_nap():
                try:

                    so_tien_str = ent_so_tien.get().replace(",", "").replace(".", "")
                    so_tien_nap = float(so_tien_str)
                    
                    if so_tien_nap <= 0:
                        messagebox.showerror("Lỗi", "Số tiền nạp phải lớn hơn 0!")
                        return
                    
                    kh = dskh.tim_theo_ma(ma_kh)
                    if kh:

                        kh.so_tien += so_tien_nap
                        
                        dskh.file.save_data()
                        
                        luu(ma_kh, ten_kh, so_tien_nap)
        
                        messagebox.showinfo("Thành công", f"Đã nạp {so_tien_nap:,.0f} VNĐ cho {ten_kh}.\nSố dư mới: {kh.so_tien:,.0f} VNĐ")
                        
                        capnhat(dskh.list)
                        f_nap.destroy()
                    else:
                        messagebox.showerror("Lỗi", "Không tìm thấy khách hàng!")
        
                except ValueError:
                    messagebox.showerror("Lỗi", "Vui lòng nhập số tiền hợp lệ!")
        
            tk.Button(f_nap, text="XÁC NHẬN NẠP", command=xac_nhan_nap, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), height=2).pack(pady=20, padx=30, fill="x")
            f_nap.bind('<Return>', lambda e: xac_nhan_nap())
            
        def luu(ma_kh, ten_kh, so_tien_nap):
            folder_path = "./json/lichsunap"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            file_path = os.path.join(folder_path, "lich_su_nap_tien.json")
            history = []
            
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try: history = json.load(f)
                    except: history = []
        
            history.append({
                "ma_nhan_vien": ma,
                "ma_khach_hang": ma_kh,
                "ten_khach_hang": ten_kh,
                "so_tien_nap": so_tien_nap,
                "thoi_gian_nap": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)   
                
        def xemlichsunap():
            
            f_lsu = tk.Toplevel()
            f_lsu.title("Lịch sử nạp tiền khách hàng")
            f_lsu.geometry("800x500")
            f_lsu.configure(bg="#f5f6fa")
            f_lsu.grab_set()
        
            
            tk.Label(
                f_lsu, 
                text="NHẬT KÝ GIAO DỊCH NẠP TIỀN", 
                font=("Arial", 14, "bold"), 
                bg="#f5f6fa", 
                fg="#2f3640"
            ).pack(pady=15)
        
            
            frame = tk.Frame(f_lsu)
            frame.pack(fill="both", expand=True, padx=20, pady=5)
        
            columns = ("ma_kh", "ten_kh", "so_tien", "thoi_gian")
            tr_lsu = ttk.Treeview(frame, columns=columns, show="headings")
        
            
            tr_lsu.heading("ma_kh", text="Mã Khách Hàng")
            tr_lsu.heading("ten_kh", text="Tên Khách Hàng")
            tr_lsu.heading("so_tien", text="Số Tiền Nạp")
            tr_lsu.heading("thoi_gian", text="Thời Gian Giao Dịch")
        
            
            tr_lsu.column("ma_kh", width=120, anchor="center")
            tr_lsu.column("ten_kh", width=200, anchor="w")
            tr_lsu.column("so_tien", width=150, anchor="e")
            tr_lsu.column("thoi_gian", width=200, anchor="center")
        
           
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tr_lsu.yview)
            tr_lsu.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            tr_lsu.pack(fill="both", expand=True)
        
            
            file_path = "./json/lichsunap/lich_su_nap_tien.json"
            tong_dichduh_thu = 0
            
            with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)

                        for item in reversed(data):
                            st = item.get("so_tien_nap", 0)
                            tong_dichduh_thu += st
                            
                            tr_lsu.insert("", "end", values=(
                                item.get("ma_khach_hang"),
                                item.get("ten_khach_hang"),
                                f"{st:,.0f} VNĐ",
                                item.get("thoi_gian_nap")
                            ))
                    except:
                        pass
        
            lbl_tong = tk.Label(
                f_lsu, 
                text=f"TỔNG TIỀN ĐÃ NẠP: {tong_dichduh_thu:,.0f} VNĐ", 
                font=("Arial", 11, "bold"), 
                bg="#f5f6fa", 
                fg="#c23616"
            )
            lbl_tong.pack(pady=10)
        
            tk.Button(
                f_lsu, 
                text="ĐÓNG", 
                command=f_lsu.destroy, 
                bg="#7f8c8d", 
                fg="white", 
                width=15
            ).pack(pady=10)
            
        def doigio():

            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Thông báo", "Vui lòng chọn khách hàng muốn mua giờ!")
                return
        
            item_data = tr.item(chon)['values']
            ma_kh = item_data[0]
            ten_kh = item_data[1]
            so_tien_hien_co = float(item_data[4])
        

            f_mua = tk.Toplevel(skh)
            f_mua.title("Đổi giờ chơi")
            f_mua.geometry("300x250")
            f_mua.configure(bg="#f0f0f0")
        
            tk.Label(f_mua, text=f"Khách hàng: {ten_kh}", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=10)
            tk.Label(f_mua, text=f"Số dư hiện tại: {so_tien_hien_co:,.0f} VNĐ", fg="blue", bg="#f0f0f0").pack()
            
            tk.Label(f_mua, text="Nhập số tiền muốn đổi sang giờ:", bg="#f0f0f0").pack(pady=5)
            ent_tien_doi = tk.Entry(f_mua, font=("Arial", 12))
            ent_tien_doi.pack(pady=5)
            
            tk.Label(f_mua, text="(Tỉ lệ: 10,000đ = 1 giờ)", font=("Arial", 8, "italic"), bg="#f0f0f0").pack()
        
            def xndoi():
                try:
                    tien_doi = float(ent_tien_doi.get())
                    
                    if tien_doi > so_tien_hien_co:
                        messagebox.showerror("Lỗi", "Số dư tài khoản không đủ để thực hiện giao dịch này!")
                        return
                    if tien_doi < 1000:
                        messagebox.showerror("Lỗi", "Số tiền đổi tối thiểu là 1,000đ!")
                        return
        
                    don_gia = 10000
                    gio_them = tien_doi / don_gia 
        
                    kh = dskh.tim_theo_ma(ma_kh)
                    if kh:
                        kh.so_tien -= tien_doi  
                        kh.gio_choi += gio_them 
                        
                        dskh.file.save_data()
                        
                        messagebox.showinfo("Thành công", f"Đã đổi {tien_doi:,.0f} VNĐ thành {gio_them:.2f} giờ chơi!")
                        capnhat(dskh.list) 
                        f_mua.destroy()
                        
                except ValueError:
                    messagebox.showerror("Lỗi", "Vui lòng nhập số tiền hợp lệ!")
        
            tk.Button(f_mua, text="Xác nhận đổi giờ", command=xndoi, bg="#007bff", fg="white", font=("Arial", 10, "bold")).pack(pady=20)
        
        def themKH():
            if vt =="quản trị":
                
                form = tk.Toplevel(skh)
                form.title("Thêm khách hàng mới")
                form.geometry("300x400")
            
                tk.Label(form, text="Mã khách:").pack()
                enma = tk.Entry(form)
                enma.pack()
            
                tk.Label(form, text="Tên khách:").pack()
                enten = tk.Entry(form)
                enten.pack()
            
                tk.Label(form, text="Số điện thoại:").pack()
                ensdt = tk.Entry(form)
                ensdt.pack()
            
                tk.Label(form, text="Tài khoản:").pack()
                entk = tk.Entry(form)
                entk.pack()
            
                tk.Label(form, text="Mật khẩu:").pack()
                enmk = tk.Entry(form, show="*")
                enmk.pack()
            else:
                messagebox.showerror("Lỗi","Bạn không có quyền")
                return
            def xnthem():
                    ma=enma.get().strip().upper()
                    if not re.match(r"^KH\d{3}$", ma):
                        messagebox.showerror("Lỗi định dạng", "Mã máy phải bắt đầu bằng KH và theo sau bởi 2 chữ số!\nVí dụ: KH01, KH99")
                        return
                    ten=" ".join(enten.get().strip().split()).title()
                    sdt=ensdt.get().strip()
                    if not re.match(r"^0\d{9}$", sdt):
                        messagebox.showerror("Lỗi định dạng", "Số điện thoại phải bắt đầu bằng số 0 và có đúng 10 chữ số!\nVí dụ: 0123456789")
                        return
                    tk=entk.get().strip()
                    mk=enmk.get().strip()
                    if ma=="" or ten=="" or sdt=="" or tk=="" or mk=="":
                        messagebox.showerror("Lỗi","Vui lòng nhập đầy đủ thông tin!")
                        return
                    moi = KhachHang(
                    ma, ten, sdt,
                    tk, mk, 0, 0)
                

                    success, message = dskh.them(moi)
                
                    if success:
                        messagebox.showinfo("Thông báo", message)
                        capnhat(dskh.list)
                        form.destroy()
                    else:
                        messagebox.showerror("Lỗi", message)
            
            tk.Button(form, text="Lưu khách hàng", command=xnthem).pack(pady=20)
            
        
        def xoaKH():
            if vt =="quản trị":
                chon = tr.selection()
                
                if not chon:
                    messagebox.showwarning("Thông báo", "Vui lòng chọn khách hàng cần xóa từ DVnh sách!")
                    return
            
                item = tr.item(chon)
                ma_kh = item['values'][0]
                ten_kh = item['values'][1]
            
                tra_loi = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa khách hàng:\n[{ma_kh}] - {ten_kh} không?")
                
                if tra_loi:
                    success, message = dskh.xoa(ma_kh)
                    
                    if success:
                        messagebox.showinfo("Thành công", message)
                        capnhat(dskh.list) 
                    else:
                        messagebox.showerror("Lỗi", message)
            else:
                messagebox.showerror("Lỗi","Bạn không có quyền")
                
        def suaKH():

            if vt != "quản trị":
                messagebox.showerror("Lỗi", "Bạn không có quyền thực hiện chức năng này!")
                return
        
            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Thông báo", "Vui lòng chọn khách hàng cần sửa!")
                return
        
            item_data = tr.item(chon)['values']
            ma_cu = item_data[0]
            kh_goc = dskh.tim_theo_ma(ma_cu)
        
            if not kh_goc:
                messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu khách hàng gốc!")
                return
        
            f_sua = tk.Toplevel(skh)
            f_sua.title(f"Sửa khách hàng: {ma_cu}")
            f_sua.geometry("350x450")
            f_sua.resizable(False, False)
            f_sua.grab_set()
        
      
            tk.Label(f_sua, text=f"CHỈNH SỬA THÔNG TIN", font=("Arial", 12, "bold")).pack(pady=10)
        
            tk.Label(f_sua, text="Tên khách:").pack(pady=(5, 0))
            enten = tk.Entry(f_sua, font=("Arial", 10))
            enten.insert(0, kh_goc.ten_khach)
            enten.pack(pady=5, padx=20, fill="x")
        
            tk.Label(f_sua, text="Số điện thoại:").pack(pady=(5, 0))
            ensdt = tk.Entry(f_sua, font=("Arial", 10))

            ensdt.insert(0, str(kh_goc.so_dien_thoai).zfill(10)) 
            ensdt.pack(pady=5, padx=20, fill="x")
        
            tk.Label(f_sua, text="Mật khẩu:").pack(pady=(5, 0))
            enmk = tk.Entry(f_sua, font=("Arial", 10), show="*")
            enmk.insert(0, kh_goc.mat_khau)
            enmk.pack(pady=5, padx=20, fill="x")
        
            def xnsua():
                ten=" ".join(enten.get().strip().split()).title()
                sdt=ensdt.get().strip()
                if not re.match(r"^0\d{9}$", sdt):
                    messagebox.showerror("Lỗi định dạng", "Số điện thoại phải bắt đầu bằng số 0 và có đúng 10 chữ số!\nVí dụ: 0123456789")
                    return
                mk=enmk.get().strip()

                KhachHangClass = type(kh_goc)
                
                kh_moi = KhachHangClass(
                    kh_goc.ma_khach,
                    ten,
                    sdt,
                    kh_goc.tai_khoan,
                    mk,
                    kh_goc.so_tien,
                    kh_goc.gio_choi
                )
        
                success, message = dskh.sua(kh_moi)
                
                if success:
                    capnhat(dskh.list)  
                    messagebox.showinfo("Thành công", "Đã cập nhật thông tin khách hàng!")
                    f_sua.destroy()
                else:
                    messagebox.showerror("Lỗi", message)
        
            tk.Button(
                f_sua, 
                text="CẬP NHẬT", 
                command=xnsua, 
                bg="#27ae60", 
                fg="white", 
                font=("Arial", 10, "bold"),
                height=2
            ).pack(pady=30, padx=20, fill="x")
                

        def timKH():
            f_tim = tk.Toplevel(skh)
            f_tim.title("Tìm kiếm khách hàng")
            f_tim.geometry("300x220")
            f_tim.configure(bg="#f0f0f0")
            f_tim.grab_set()
        
            tk.Label(f_tim, text="Nhập từ khóa:", bg="#f0f0f0").pack(pady=5)
            ent_tu = tk.Entry(f_tim, font=("Arial", 11))
            ent_tu.pack(pady=5, padx=20, fill="x")
            ent_tu.focus_set()
        
            tk.Label(f_tim, text="Tìm theo:", bg="#f0f0f0").pack(pady=5)
            cb_loai = ttk.Combobox(f_tim, values=["Mã khách", "Tên khách"], state="readonly")
            cb_loai.current(0)
            cb_loai.pack(pady=5)
        
            def tim():
                tu_khoa = ent_tu.get().strip()
                
                loai_tim = cb_loai.get()
                
                if not tu_khoa:
                    messagebox.showwarning("Chú ý", "Vui lòng nhập từ khóa!")
                    return
        
                if loai_tim == "Mã khách":
                    if not re.match(r"^KH\d{3}$", tu_khoa.upper()):
                        messagebox.showerror("Lỗi định dạng", "Mã máy phải bắt đầu bằng KH và theo sau bởi 3 chữ số!\nVí dụ: KH001, KH999")
                        return

                    obj = dskh.tim_theo_ma(tu_khoa)
                    ket_qua = [obj] if obj else []
                else:
                    ket_qua = dskh.tim_theo_ten(tu_khoa)
                # ------------------------------------
        
                if ket_qua:
                    capnhat(ket_qua) 
                    f_tim.destroy()
                else:
                    messagebox.showinfo("Kết quả", f"Không tìm thấy khách hàng: {tu_khoa}")
        
            tk.Button(f_tim, text="TÌM KIẾM", command=tim, bg="#4CAF50", fg="white", width=15).pack(pady=15)
            tk.Button(f_tim, text="Hiện tất cả", command=lambda: capnhat(dskh.list), bg="#4CAF50", fg="white", width=15).pack(pady=15)
            f_tim.bind('<Return>', lambda e: tim()) 
        
        def doimk():

            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Thông báo", "Vui lòng chọn khách hàng cần đổi mật khẩu!")
                return
        
            item_data = tr.item(chon)['values']
            ma_kh = item_data[0]
            ten_kh = item_data[1]
        
            f_pass = tk.Toplevel(skh)
            f_pass.title("Đổi mật khẩu")
            f_pass.geometry("300x250")
            f_pass.configure(bg="#f0f0f0")
        
            tk.Label(f_pass, text=f"Đổi mật khẩu cho: {ten_kh}", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=10)
            
            tk.Label(f_pass, text="Mật khẩu mới:", bg="#f0f0f0").pack()
            enmk_moi = tk.Entry(f_pass, show="*", font=("Arial", 11))
            enmk_moi.pack(pady=5)
        
            tk.Label(f_pass, text="Xác nhận mật khẩu mới:", bg="#f0f0f0").pack()
            ent_xac_nhan = tk.Entry(f_pass, show="*", font=("Arial", 11))
            ent_xac_nhan.pack(pady=5)
        
            def xndoi():
                mk_moi = enmk_moi.get()
                mk_xac_nhan = ent_xac_nhan.get()

                if len(mk_moi) < 1:
                    messagebox.showerror("Lỗi", "Mật khẩu không được để trống!")
                    return
                
                if mk_moi != mk_xac_nhan:
                    messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
                    return
        
                kh = dskh.tim_theo_ma(ma_kh)
                if kh:
                    kh.mat_khau = mk_moi
                    dskh.file.save_data() 
                    
                    messagebox.showinfo("Thành công", f"Đã đổi mật khẩu thành công cho khách hàng {ten_kh}")
                    f_pass.destroy()
                else:
                    messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu khách hàng!")
        
            tk.Button(f_pass, text="Cập nhật mật khẩu", command=xndoi, bg="#dc3545", fg="white", font=("Arial", 10, "bold")).pack(pady=15)    
        
        def xemchitiet():
            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Thông báo", "Vui lòng chọn một khách hàng để xem chi tiết!")
                return

            item_data = tr.item(chon)['values']
            ma_kh = item_data[0]

            kh = dskh.tim_theo_ma(ma_kh)
            
            if kh:

                f_detail = tk.Toplevel(skh)
                f_detail.title(f"Chi tiết khách hàng: {kh.ten_khach}")
                f_detail.geometry("350x450")
                f_detail.configure(bg="#ffffff")
        
                tk.Label(f_detail, text="THÔNG TIN CHI TIẾT", font=("Arial", 14, "bold"), bg="#ffffff", fg="#333").pack(pady=15)
        
                info_frame = tk.Frame(f_detail, bg="#ffffff")
                info_frame.pack(padx=20, fill="x")
        
                def add_info_row(label_text, value_text, color="black"):
                    row = tk.Frame(info_frame, bg="#ffffff")
                    row.pack(fill="x", pady=5)
                    tk.Label(row, text=label_text, font=("Arial", 10, "bold"), bg="#ffffff", width=15, anchor="w").pack(side="left")
                    tk.Label(row, text=value_text, font=("Arial", 10), bg="#ffffff", fg=color, anchor="w").pack(side="left")
        
                add_info_row("Mã khách:", kh.ma_khach)
                add_info_row("Tên khách:", kh.ten_khach)
                add_info_row("Số điện thoại:", kh.so_dien_thoai)
                add_info_row("Tài khoản:", kh.tai_khoan)
                
                add_info_row("Mật khẩu:", kh.mat_khau, "red") 
                
                add_info_row("Số dư tiền:", f"{kh.so_tien:,.0f} VNĐ", "green")
                add_info_row("Giờ chơi:", f"{kh.gio_choi:.2f} giờ", "blue")
        

                tk.Button(f_detail, text="Đóng", command=f_detail.destroy, width=15, bg="#808080", fg="white").pack(pady=20)
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu khách hàng!")    
        def hienall():
            capnhat(dskh.list)
        def capnhat(ds):
            dskh.sap_xep_ma_tang()
            tr.delete(*tr.get_children())
            for kh in ds:           
                tr.insert("", "end", values=(kh.ma_khach,kh.ten_khach,kh.so_dien_thoai,kh.tai_khoan,kh.so_tien,kh.gio_choi))
        
        
        skh = tk.Toplevel()
        skh.title("Quản lý Khách hàng")
        skh.geometry("840x550")
        skh.configure(bg="#808080")
        skh.grab_set()

        frtc = tk.LabelFrame(skh, text="Tùy Chọn", bg="#808080", fg="white", font=("Arial", 10, "bold"))
        frtc.place(x=5, y=2, width=830, height=120)

        def tạo_icon(path):
            img = Image.open(path).resize((60, 60), Image.LANCZOS)
            return ImageTk.PhotoImage(img)

        ic_nap = tạo_icon("./img/money.png")
        btn_nap = tk.Button(skh, image=ic_nap, text="Nạp Tiền", compound="top", bg="#808080", fg="white", bd=0, command=naptienKH)
        btn_nap.image = ic_nap; btn_nap.place(x=15, y=20)

        ic_mua = tạo_icon("./img/trade.png")
        btn_mua = tk.Button(skh, image=ic_mua, text="Mua Giờ", compound="top", bg="#808080", fg="white", bd=0, command=doigio)
        btn_mua.image = ic_mua; btn_mua.place(x=95, y=20)

        ic_mk = tạo_icon("./img/settings.png")
        btn_mk = tk.Button(skh, image=ic_mk, text="Đổi MK", compound="top", bg="#808080", fg="white", bd=0, command=doimk)
        btn_mk.image = ic_mk; btn_mk.place(x=175, y=20)

        ic_all = tạo_icon("./img/clock.png")
        btn_all = tk.Button(skh, image=ic_all, text="Lịch sử", compound="top", bg="#808080", fg="white", bd=0, command=xemlichsunap)
        btn_all.image = ic_all; btn_all.place(x=255, y=20)

        ic_tim = tạo_icon("./img/find.png")
        btn_tim = tk.Button(skh, image=ic_tim, text="Tìm KH", compound="top", bg="#808080", fg="white", bd=0, command=timKH)
        btn_tim.image = ic_tim; btn_tim.place(x=335, y=20)

        ic_add = tạo_icon("./img/adduser.png")
        btn_add = tk.Button(skh, image=ic_add, text="Thêm KH", compound="top", bg="#808080", fg="white", bd=0, command=themKH)
        btn_add.image = ic_add; btn_add.place(x=415, y=20)

        ic_fix = tạo_icon("./img/profile.png")
        btn_fix = tk.Button(skh, image=ic_fix, text="Sửa TT", compound="top", bg="#808080", fg="white", bd=0, command=suaKH)
        btn_fix.image = ic_fix; btn_fix.place(x=495, y=20)

        ic_del = tạo_icon("./img/rubbishbin.png")
        btn_del = tk.Button(skh, image=ic_del, text="Xóa KH", compound="top", bg="#808080", fg="white", bd=0, command=xoaKH)
        btn_del.image = ic_del; btn_del.place(x=575, y=20)

        frtr = tk.LabelFrame(skh, text="Danh Sách Khách Hàng", bg="#808080", fg="white", font=("Arial", 10, "bold"))
        frtr.place(x=5, y=130, width=830, height=410)

        tr = ttk.Treeview(frtr, columns=("ma", "ten", "sdt", "tk", "tien", "gio"), show="headings")
        
        tr.heading("ma", text="Mã Khách"); tr.column("ma", width=80, anchor="center")
        tr.heading("ten", text="Tên Khách Hàng"); tr.column("ten", width=180, anchor="w")
        tr.heading("sdt", text="Số Điện Thoại"); tr.column("sdt", width=120, anchor="center")
        tr.heading("tk", text="Tài Khoản"); tr.column("tk", width=120, anchor="center")
        tr.heading("tien", text="Số Tiền (VNĐ)"); tr.column("tien", width=120, anchor="e")
        tr.heading("gio", text="Giờ Chơi"); tr.column("gio", width=100, anchor="center")

        tr.pack(fill="both", expand=True, padx=5, pady=5)
        
        capnhat(dskh.list)
    def nhanvien():

        def themNV():
            if vt != "quản trị":
                messagebox.showerror("Lỗi", "Chỉ Quản trị mới có quyền thêm nhân viên!")
                return

            f_them = tk.Toplevel()
            f_them.title("Thêm nhân viên mới")
            f_them.geometry("380x620") 
            f_them.grab_set()

           
            tk.Label(f_them, text="Mã NV (NVxxx):").pack(pady=2)
            ent_ma = tk.Entry(f_them); ent_ma.pack()

            tk.Label(f_them, text="Tên nhân viên:").pack(pady=2)
            ent_ten = tk.Entry(f_them); ent_ten.pack()

            tk.Label(f_them, text="Số điện thoại:").pack(pady=2)
            ent_sdt = tk.Entry(f_them); ent_sdt.pack()

            tk.Label(f_them, text="Tên đăng nhập:").pack(pady=2)
            ent_tk = tk.Entry(f_them); ent_tk.pack()

            tk.Label(f_them, text="Mật khẩu:").pack(pady=2)
            ent_mk = tk.Entry(f_them, show="*"); ent_mk.pack()

            tk.Label(f_them, text="Lương:").pack(pady=2)
            ent_luong = tk.Entry(f_them); ent_luong.pack()

            tk.Label(f_them, text="Vai trò:").pack(pady=2)
            cb_vt = ttk.Combobox(f_them, values=["quản trị", "nhân viên"], state="readonly")
            cb_vt.current(1); cb_vt.pack()

            def xnthem():
                ma = ent_ma.get().strip().upper()
                if not re.match(r"^NV\d{3}$", ma):
                    messagebox.showerror("Lỗi", "Mã phải có dạng NVxxx!")
                    return
                
                luong = ent_luong.get().strip()
                if not luong.isdigit():
                    messagebox.showerror("Lỗi", "Lương phải là con số!")
                    return
                if int(luong) <= 0:
                    messagebox.showerror("Lỗi", "Lương phải lớn hơn 0!")
                    return
                ten=" ".join(ent_ten.get().strip().split()).title()
                sdt=ent_sdt.get().strip()
                tk=ent_tk.get().strip()
                mk=ent_mk.get().strip()
                if ma=="" or ten=="" or sdt=="" or tk=="" or mk=="":
                    messagebox.showerror("Lỗi","Vui lòng nhập đầy đủ thông tin!")
                    return
                moi = NhanVien(
                    ma, 
                    ent_ten.get().strip(), 
                    ent_sdt.get().strip(), 
                    ent_tk.get().strip(), 
                    ent_mk.get().strip(), 
                    cb_vt.get(),
                    int(luong)
                )
                
                success, msg = dsnv.them(moi)
                if success:
                    messagebox.showinfo("Thành công", msg)
                    capnhat(dsnv.list)
                    f_them.destroy()
                else:
                    messagebox.showerror("Lỗi", msg)

            tk.Button(f_them, text="XÁC NHẬN THÊM", bg="#2ecc71", fg="white", 
                    font=("Arial", 10, "bold"), command=xnthem).pack(pady=20)
                    
        def suaNV():
            if vt != "quản trị":
                messagebox.showerror("Lỗi", "Bạn không có quyền sửa thông tin!")
                return

            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Chú ý", "Hãy chọn một nhân viên để sửa!")
                return

            ma_nv = tr.item(chon)['values'][0]
            nv_cu = dsnv.tim_theo_ma(ma_nv)

            f_sua = tk.Toplevel()
            f_sua.title(f"Sửa NV: {ma_nv}")
            f_sua.geometry("380x600")
            f_sua.grab_set()

            tk.Label(f_sua, text="Tên nhân viên:").pack(pady=2)
            ent_ten = tk.Entry(f_sua); ent_ten.insert(0, nv_cu.ten_nhan_vien); ent_ten.pack()

            tk.Label(f_sua, text="Số điện thoại:").pack(pady=2)
            ent_sdt = tk.Entry(f_sua); ent_sdt.insert(0, nv_cu.so_dien_thoai); ent_sdt.pack()

            tk.Label(f_sua, text="Mật khẩu:").pack(pady=2)
            ent_mk = tk.Entry(f_sua); ent_mk.insert(0, nv_cu.mat_khau); ent_mk.pack()

            tk.Label(f_sua, text="Lương:").pack(pady=2)
            ent_luong = tk.Entry(f_sua); ent_luong.insert(0, str(nv_cu.luong)); ent_luong.pack()

            tk.Label(f_sua, text="Vai trò:").pack(pady=2)
            cb_vt = ttk.Combobox(f_sua, values=["quản trị", "nhân viên"], state="readonly")
            cb_vt.set(nv_cu.vai_tro); cb_vt.pack()

            def xnsua():
                luong_moi = ent_luong.get().strip()
                if not luong_moi.isdigit():
                    messagebox.showerror("Lỗi", "Lương phải là số!")
                    return
                if int(luong_moi) <= 0:
                    messagebox.showerror("Lỗi", "Lương phải lớn hơn 0!")
                    return
                ten=" ".join(ent_ten.get().strip().split()).title()
                sdt=ent_sdt.get().strip()
                mk=ent_mk.get().strip()
                if ma_nv=="" or ten=="" or sdt=="" or mk=="":
                    messagebox.showerror("Lỗi","Vui lòng nhập đầy đủ thông tin!")
                    return
                if not re.match(r"^0\d{9}$", sdt):
                    messagebox.showerror("Lỗi định dạng", "Số điện thoại phải bắt đầu bằng số 0 và có đúng 10 chữ số!\nVí dụ: 0123456789")
                    return
                
                nv_moi = NhanVien(
                    ma_nv, 
                    ent_ten.get().strip(), 
                    ent_sdt.get().strip(), 
                    nv_cu.ten_dang_nhap,
                    ent_mk.get().strip(), 
                    cb_vt.get(),
                    int(luong_moi)
                )
                
                success, msg = dsnv.sua(nv_moi)
                if success:
                    messagebox.showinfo("Thành công", "Đã cập nhật dữ liệu!")
                    capnhat(dsnv.list)
                    f_sua.destroy()
                else:
                    messagebox.showerror("Lỗi", msg)

            tk.Button(f_sua, text="LƯU THAY ĐỔI", bg="#3498db", fg="white", 
                    font=("Arial", 10, "bold"), command=xnsua).pack(pady=20)
                
        def xoaNV():
            if vt != "quản trị":
                messagebox.showerror("Lỗi", "Chỉ Quản trị mới được phép xóa nhân viên!")
                return

            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Thông báo", "Chọn nhân viên muốn xóa!")
                return

            ma_nv = tr.item(chon)['values'][0]
            

            if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhân viên {ma_nv}?"):
                success, msg = dsnv.xoa(ma_nv)
                if success:
                    messagebox.showinfo("Thành công", msg)
                    capnhat(dsnv.list)
                else:
                    messagebox.showerror("Lỗi", msg)
        
        def timNV():
            f_tim = tk.Toplevel()
            f_tim.title("Tìm kiếm nhân viên")
            f_tim.geometry("350x250")
            f_tim.grab_set()
            f_tim.configure(bg="#f0f0f0")

            tk.Label(f_tim, text="Nhập từ khóa cần tìm:", font=("Arial", 10), bg="#f0f0f0").pack(pady=10)
            ent_tu = tk.Entry(f_tim, font=("Arial", 10), width=30)
            ent_tu.pack(pady=5)

            tk.Label(f_tim, text="Tìm theo:", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
            cb_loai = ttk.Combobox(f_tim, values=["Mã nhân viên", "Tên nhân viên"], state="readonly", font=("Arial", 10))
            cb_loai.current(0) 
            cb_loai.pack(pady=5)

            def tim():
                tu = ent_tu.get().strip()
                if not tu:
                    messagebox.showwarning("Chú ý", "Vui lòng nhập từ khóa tìm kiếm!")
                    return

                loai = cb_loai.get()
                ket_qua = []

                if loai == "Mã nhân viên":
                    if not re.match(r"^NV\d{3}$", tu.upper()):
                        messagebox.showerror("Lỗi định dạng", "Mã phải có dạng NVxxx!\nVí dụ: NV001, NV123")
                        return
                    nv = dsnv.tim_theo_ma(tu)
                    if nv:
                        ket_qua = [nv]
                else:
                    tu=" ".join(tu.split()).title()
                    ket_qua = dsnv.tim_theo_ten(tu)

                if ket_qua:

                    capnhat(ket_qua)
                    f_tim.destroy()
                else:
                    messagebox.showinfo("Thông báo", f"Không tìm thấy nhân viên nào phù hợp với: {tu}")

            tk.Button(f_tim, text="TÌM KIẾM", bg="#3498db", fg="white", font=("Arial", 10, "bold"), 
                    width=15, command=tim).pack(pady=20)
        
        def doimkNV():

            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Thông báo", "Vui lòng chọn một nhân viên từ DVnh sách để đổi mật khẩu!")
                return

            machon = tr.item(chon)['values'][0]
            vtchon = tr.item(chon)['values'][3]
            nv_target = dsnv.tim_theo_ma(machon)

            if not nv_target:
                messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu nhân viên!")
                return
            if vt == "nhân viên":
                if machon != ma:
                    messagebox.showerror("Từ chối", "Bạn không có quyền đổi mật khẩu của nhân viên khác!")
                    return
            else:
                if vtchon == "quản trị" and machon != ma:
                    messagebox.showerror("Từ chối", "Bạn không có quyền đổi mật khẩu của Quản trị viên khác!")
                    return
            f_mk = tk.Toplevel()
            f_mk.title(f"Đổi mật khẩu - {machon}")
            f_mk.geometry("350x300")
            f_mk.grab_set()
            f_mk.configure(bg="#f0f0f0")

            tk.Label(f_mk, text=f"Đổi mật khẩu cho: {nv_target.ten_nhan_vien}", 
                    font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=15)

            tk.Label(f_mk, text="Mật khẩu mới:", bg="#f0f0f0").pack(pady=5)
            ent_mk_moi = tk.Entry(f_mk, show="*", font=("Arial", 10), width=25)
            ent_mk_moi.pack()

            tk.Label(f_mk, text="Xác nhận mật khẩu:", bg="#f0f0f0").pack(pady=5)
            ent_xac_nhan = tk.Entry(f_mk, show="*", font=("Arial", 10), width=25)
            ent_xac_nhan.pack()

            def xac_nhan_doi():
                mk_moi = ent_mk_moi.get().strip()
                xac_nhan = ent_xac_nhan.get().strip()

                if len(mk_moi) < 1:
                    messagebox.showerror("Lỗi", "Mật khẩu không được để trống!")
                    return
                
                if mk_moi != xac_nhan:
                    messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
                    return
                
                nv_cap_nhat = NhanVien(
                    nv_target.ma_nhan_vien,
                    nv_target.ten_nhan_vien,
                    nv_target.so_dien_thoai,
                    nv_target.ten_dang_nhap,
                    mk_moi, 
                    nv_target.vai_tro,
                    nv_target.luong
                )

                success, msg = dsnv.sua(nv_cap_nhat)
                if success:
                    messagebox.showinfo("Thành công", f"Đã đổi mật khẩu cho nhân viên {machon}")
                    f_mk.destroy()
                else:
                    messagebox.showerror("Lỗi", msg)

            tk.Button(f_mk, text="XÁC NHẬN ĐỔI", bg="#e67e22", fg="white", 
                    font=("Arial", 10, "bold"), width=15, command=xac_nhan_doi).pack(pady=25)
        
        def chitietNV():
                chon = tr.selection()
                if not chon:
                    messagebox.showwarning("Thông báo", "Vui lòng chọn một nhân viên!")
                    return

                machon = tr.item(chon)['values'][0]
                vtchon = tr.item(chon)['values'][3]

                if vt == "nhân viên":

                    if machon != ma:
                        messagebox.showerror("Từ chối", "Bạn không có quyền xem chi tiết của nhân viên khác!")
                        return
                # ---------------------------
                else:
                    if vtchon == "quản trị" and machon != ma:
                        messagebox.showerror("Từ chối", "Bạn không có quyền xem chi tiết của Quản trị viên khác!")
                        return
                nv = dsnv.tim_theo_ma(machon)
                if not nv: return
            
                f_ct = tk.Toplevel()
                f_ct.title(f"Chi tiết nhân viên - {machon}")
                f_ct.geometry("400x550")
                f_ct.grab_set()
            
                tk.Label(f_ct, text="THÔNG TIN CHI TIẾT", font=("Arial", 14, "bold")).pack(pady=20)
                fr_info = tk.Frame(f_ct, bg="white", bd=1, relief="solid")
                fr_info.pack(padx=20, fill="both", expand=True)
            
                def tao_dong(label_text, value_text):
                    row = tk.Frame(fr_info, bg="white")
                    row.pack(fill="x", padx=15, pady=8)
                    tk.Label(row, text=label_text, font=("Arial", 10, "bold"), bg="white", width=15, anchor="w").pack(side="left")
                    ent = tk.Entry(row, font=("Arial", 10), bg="white", bd=0)
                    ent.insert(0, value_text)
                    ent.config(state="readonly")
                    ent.pack(side="left", fill="x", expand=True)
            
           
                tao_dong("Mã nhân viên:", nv.ma_nhan_vien)
                tao_dong("Họ và tên:", nv.ten_nhan_vien)
                tao_dong("Số điện thoại:", nv.so_dien_thoai)
                tao_dong("Tài khoản:", nv.ten_dang_nhap)
                tao_dong("Vai trò:", nv.vai_tro.upper())
                
              
                try:
                    luong_val = int(nv.luong)
                    tao_dong("Mức lương:", f"{luong_val:,} VNĐ")
                except:
                    tao_dong("Mức lương:", "0 VNĐ")
                    
                tao_dong("Mật khẩu:", nv.mat_khau)
            
                tk.Button(f_ct, text="ĐÓNG", command=f_ct.destroy).pack(pady=20)
                                            
        def capnhat(ds):
            dsnv.sap_xep_ma_tang() 
            tr.delete(*tr.get_children())
            for nv in ds:
                tr.insert("", "end", values=(
                    nv.ma_nhan_vien,   
                    nv.ten_nhan_vien,  
                    nv.ten_dang_nhap,  
                    nv.vai_tro,       
                    nv.so_dien_thoai   
                ))

        snv = tk.Toplevel() 
        snv.title("Quản lý nhân viên")
        snv.geometry("840x550")
        snv.configure(bg="#808080")
        snv.grab_set()

        frtc = tk.LabelFrame(snv, text="Tùy Chọn", bg="#808080", fg="white", font=("Arial", 10, "bold"))
        frtc.place(x=5, y=2, width=830, height=120)

        ictc = ImageTk.PhotoImage(Image.open("./img/find.png").resize((64, 64), Image.LANCZOS))
        btn_tc = tk.Button(snv, image=ictc, text="Tìm NV", compound="top", bg="#808080", fg="white", bd=0, command=timNV)
        btn_tc.image = ictc
        btn_tc.place(x=10, y=20)

        icsua = ImageTk.PhotoImage(Image.open("./img/profile.png").resize((64, 64), Image.LANCZOS))
        btn_sua = tk.Button(snv, image=icsua, text="Đổi MK", compound="top", bg="#808080", fg="white", bd=0, command=doimkNV)
        btn_sua.image = icsua
        btn_sua.place(x=90, y=20)

        icxoa = ImageTk.PhotoImage(Image.open("./img/controlpanel.png").resize((64, 64), Image.LANCZOS))
        btn_xoa = tk.Button(snv, image=icxoa, text="Chi tiết", compound="top", bg="#808080", fg="white", bd=0, command=chitietNV)
        btn_xoa.image = icxoa
        btn_xoa.place(x=170, y=20)
        
        ictc = ImageTk.PhotoImage(Image.open("./img/plus.png").resize((64, 64), Image.LANCZOS))
        btn_tc = tk.Button(snv, image=ictc, text="Thêm NV", compound="top", bg="#808080", fg="white", bd=0, command=themNV)
        btn_tc.image = ictc
        btn_tc.place(x=260, y=20)

        icsua = ImageTk.PhotoImage(Image.open("./img/update.png").resize((64, 64), Image.LANCZOS))
        btn_sua = tk.Button(snv, image=icsua, text="Sửa NV", compound="top", bg="#808080", fg="white", bd=0, command=suaNV)
        btn_sua.image = icsua
        btn_sua.place(x=350, y=20)

        icxoa = ImageTk.PhotoImage(Image.open("./img/delete.png").resize((64, 64), Image.LANCZOS))
        btn_xoa = tk.Button(snv, image=icxoa, text="Xóa NV", compound="top", bg="#808080", fg="white", bd=0, command=xoaNV)
        btn_xoa.image = icxoa
        btn_xoa.place(x=440, y=20)

        frtr = tk.LabelFrame(snv, text="Thông tin Nhân Viên", bg="#808080", fg="white", font=("Arial", 10, "bold"))
        frtr.place(x=2, y=130, width=830, height=400)

        tr = ttk.Treeview(snv, columns=("ma", "ten", "tk", "vt", "sdt"), show="headings")

        tr.heading("ma", text="Mã NV")
        tr.heading("ten", text="Tên nhân viên")
        tr.heading("tk", text="Tài khoản")
        tr.heading("vt", text="Vai trò")
        tr.heading("sdt", text="Số điện thoại")

        tr.column("ma", width=80, anchor="center")
        tr.column("ten", width=200, anchor="w")
        tr.column("tk", width=150, anchor="center")
        tr.column("vt", width=120, anchor="center")
        tr.column("sdt", width=150, anchor="center")

        tr.place(x=10, y=150, width=810, height=360)

        capnhat(dsnv.list)
        snv.mainloop()
    def maytinh(): 
        
        def themmay():
            if vt=="quản trị":
                popup = tk.Toplevel(smt)
                popup.title("Thêm máy mới")
                popup.geometry("300x200")
                popup.resizable(False, False)
                
                popup.grab_set() 
    
                tk.Label(popup, text="Mã máy:").pack(pady=(10, 0))
                enma = tk.Entry(popup)
                enma.pack(pady=5)
    
                tk.Label(popup, text="Loại máy:").pack(pady=(10, 0))
    
                cbo_loai = ttk.Combobox(popup, values=["thường", "VIP"], state="readonly")
                cbo_loai.set("thường")
                cbo_loai.pack(pady=5)
    
                def xnth():
                    ma = enma.get().strip()
                    loai = cbo_loai.get()
                    
                    if not re.match(r"^PC\d{2}$", ma):
                        messagebox.showerror("Lỗi định dạng", "Mã máy phải bắt đầu bằng PC và theo sau bởi 2 chữ số!\nVí dụ: PC01, PC99")
                        return
                    if not ma:
                        messagebox.showerror("Lỗi", "Vui lòng nhập mã máy!")
                        return
    
                    if len(dsmt.list) > 0:
                        MayTinhClass = type(dsmt.list[0])
                        moi = MayTinhClass(ma, loai, "trống")
                        
                        thanh_cong, thong_bao = dsmt.them(moi)
                        
                        if thanh_cong:
                            capnhat(dsmt.list)
                            messagebox.showinfo("Thành công", thong_bao)
                            popup.destroy()
                        else:
                            messagebox.showerror("Lỗi", thong_bao)
                    else:
                        messagebox.showerror("Lỗi", "DVnh sách mẫu trống!")
    
                tk.Button(popup, text="Thêm ngay", command=xnth, bg="green", fg="white").pack(pady=20)
            else:
                messagebox.showerror("Lỗi","Bạn không có quyền")
                return
        def xoamay():
            if vt=="quản trị":
                chon = tr.selection()
                if not chon:
                    messagebox.showwarning("Chú ý", "Hãy chọn máy cần xóa!")
                    return
                
                ma_may = tr.item(chon[0], "values")[0]
                
                if ma_may in phien_may:
                    messagebox.showerror("Lỗi", "Máy đang có người dùng, không thể xóa!")
                    return
    
                if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa máy {ma_may}?"):
                    thanh_cong, thong_bao = dsmt.xoa(ma_may)
                    if thanh_cong:
                        capnhat(dsmt.list)
                        messagebox.showinfo("Thành công", thong_bao)
                    else:
                        messagebox.showerror("Lỗi", thong_bao)
            else:
                messagebox.showerror("Lỗi","Bạn không có quyền")
                return
        def suamay():
            if vt=="quản trị":

                chon = tr.selection()
                if not chon:
                    messagebox.showwarning("Chú ý", "Vui lòng chọn máy tính cần sửa từ DVnh sách!")
                    return
                
                ma_may = tr.item(chon[0], "values")[0]
                may_cu = dsmt.tim_theo_ma(ma_may) 
            
                if may_cu:

                    if may_cu.trang_thai == "đang dùng":
                        messagebox.showwarning("Cảnh báo", "Máy đang có người sử dụng, không thể sửa thông tin lúc này!")
                        return
            

                    popup_sua = tk.Toplevel(smt)
                    popup_sua.title(f"Chỉnh sửa máy: {ma_may}")
                    popup_sua.geometry("350x280")
                    popup_sua.resizable(False, False)
                    popup_sua.grab_set() 
            

                    tk.Label(popup_sua, text=f"CẬP NHẬT MÁY {ma_may}", font=("Arial", 12, "bold")).pack(pady=10)
            
                    tk.Label(popup_sua, text="Loại máy:").pack(pady=(5, 0))
                    cbo_loai = ttk.Combobox(popup_sua, values=["Thường", "VIP"], state="readonly")
                    cbo_loai.set(may_cu.loai_may) 
                    cbo_loai.pack(pady=5)
            
                    tk.Label(popup_sua, text="Tình trạng:").pack(pady=(10, 0))
                    cbo_tinh_trang = ttk.Combobox(popup_sua, values=["trống", "hỏng"], state="readonly")
                    cbo_tinh_trang.set(may_cu.trang_thai)
                    cbo_tinh_trang.pack(pady=5)

                    def luu_cap_nhat():
                        loai_moi = cbo_loai.get()
                        tinh_trang_moi = cbo_tinh_trang.get()
            
                        MayTinhClass = type(may_cu)
                        may_moi = MayTinhClass(ma_may, loai_moi, tinh_trang_moi)
                        
                        thanh_cong, thong_bao = dsmt.sua(may_moi)
                        
                        if thanh_cong:
                            capnhat(dsmt.list)
                            messagebox.showinfo("Thành công", f"Máy {ma_may} đã được cập nhật!")
                            popup_sua.destroy()
                        else:
                            messagebox.showerror("Lỗi", thong_bao)
            
                    btn_save = tk.Button(
                        popup_sua, 
                        text="LƯU THAY ĐỔI", 
                        command=luu_cap_nhat,
                        bg="#2ecc71", 
                        fg="white", 
                        font=("Arial", 10, "bold"),
                        width=20
                    )
                    btn_save.pack(pady=25)
            else:
                messagebox.showerror("Lỗi","Bạn không có quyền")
                return
        def timmay():
            f_tim = tk.Toplevel(smt)
            f_tim.title("Tìm kiếm máy tính")
            f_tim.geometry("400x150")
            f_tim.resizable(False, False)
            f_tim.configure(bg="#f0f0f0")
            
            f_tim.grab_set()

            tk.Label(f_tim, text="Nhập mã máy:", bg="#f0f0f0", font=("Arial", 10)).pack(pady=10)
            
            ent_key = tk.Entry(f_tim, width=40, font=("Arial", 10))
            ent_key.pack(pady=5)
            ent_key.focus_set()


            def thuc_hien():
                ma = ent_key.get().strip().upper()
                
                if not re.match(r"^PC\d{2}$", ma):
                    messagebox.showerror("Lỗi định dạng", "Mã máy phải bắt đầu bằng PC và theo sau bởi 2 chữ số!\nVí dụ: PC01, PC99")
                    return

                ket_qua = dsmt.tim_theo_ma(ma)
                

                capnhat(ket_qua)
                
                if not ket_qua:
                    messagebox.showinfo("Kết quả", "Không tìm thấy máy nào khớp với yêu cầu.")
                else:
                    f_tim.destroy() 

            btn_frame = tk.Frame(f_tim, bg="#f0f0f0")
            btn_frame.pack(pady=15)

            tk.Button(btn_frame, text="TÌM KIẾM", command=thuc_hien, bg="#3498db", fg="white", width=12).pack(side="left", padx=5)
            tk.Button(btn_frame, text="HỦY/HIỆN TẤT CẢ", command=lambda: [capnhat(dsmt.list), f_tim.destroy()], bg="#95a5a6", fg="white", width=15).pack(side="left", padx=5)

            f_tim.bind('<Return>', lambda e: thuc_hien())
        
        def momay():
            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Lỗi", "Vui lòng chọn máy trên DVnh sách!")
                return
    
            ma_may = tr.item(chon)["values"][0]

            may = next((m for m in dsmt.list if m.ma_may == ma_may), None)
    
            if not may: return
            if may.trang_thai != "trống":
                messagebox.showerror("Lỗi", "Máy này đang có người sử dụng!")
                return
    
            ma_khach = tk.simpledialog.askstring("Mở máy", "Nhập mã khách hàng:")
            if not ma_khach: return

            kh = next((k for k in dskh.list if k.ma_khach == ma_khach.upper()), None)
            
            if not kh:
                messagebox.showerror("Lỗi", "Không tìm thấy mã khách này!")
                return
            if kh.gio_choi <= 0:
                messagebox.showerror("Lỗi", "Tài khoản khách đã hết giờ!")
                return
    
            phien_may[ma_may] = {
                "tai_khoan": kh.tai_khoan,
                "gio": kh.gio_choi,           
                "gio_bat_DVu": kh.gio_choi,
                "ma_kh": ma_khach,
                "thoi_gian_mo": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            may.trang_thai = "đang dùng"
            capnhat(dsmt.list)
    
        def tatmay_click():
            chon = tr.selection()
            if not chon:
                messagebox.showwarning("Chú ý", "Chọn máy trước khi tắt!")
                return

            ma_may = tr.item(chon[0], "values")[0] 
            tatmay(ma_may) 
        def tatmay(ma_may):
            if ma_may not in phien_may:
                print(f"Lỗi: Máy {ma_may} không có trong phiên đang chạy.")
                return
        
            phien = phien_may.pop(ma_may)
            ma_kh = phien.get("ma_kh")
            gio_luc_DVu = phien.get("gio_bat_DVu", 0)
            gio_hien_tai = phien.get("gio", 0)
            thoi_gian_mo = phien.get("thoi_gian_mo", "Không xác định")
            
            thoi_gian_DV_choi = round(max(0, gio_luc_DVu - gio_hien_tai), 2)
            thoi_gian_tat = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            kh = next((k for k in dskh.list if k.ma_khach == ma_kh.upper()), None)
            if kh:
                kh.gio_choi = round(max(0, gio_hien_tai), 2)

                dskh.file.save_data() 
                print(f"Đã cập nhật giờ cho khách {ma_kh}: {kh.gio_choi}")
            else:
                print("Cảnh báo: Không tìm thấy khách hàng trong DVnh sách để cập nhật giờ.")
        
            lich_su_moi = {
                "ma_nhan_vien": ma,
                "ma_may": ma_may,
                "ma_kh": ma_kh,
                "tai_khoan": phien.get("tai_khoan", "N/A"),
                "gio_bat_DVu_phien": gio_luc_DVu,
                "thoi_gian_DV_choi": thoi_gian_DV_choi,
                "luc_mo_may": thoi_gian_mo,
                "luc_tat_may": thoi_gian_tat
            }
            luu(lich_su_moi)
        
            may = next((m for m in dsmt.list if m.ma_may == ma_may), None)
            if may:
                may.trang_thai = "trống"
                dsmt.file.save_data()
        
            capnhat(dsmt.list)
            messagebox.showinfo("Thông báo", f"Máy {ma_may} đã tắt.\nĐã lưu lại {kh.gio_choi if kh else 0} giờ vào tài khoản.")
        
        def luu(data):

            folder_path = "./json/lichsuchoi"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path) 
            
            file_path = os.path.join(folder_path, "lich_su_choi.json")
            history = []
            
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        history = json.load(f)
                    except:
                        history = []
                        
            history.append(data)
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
            print(f"Đã ghi lịch sử vào: {file_path}")
        
        def xemlichsu():
            f_his = tk.Toplevel(smt) 
            f_his.title("Lịch sử hoạt động máy tính")
            f_his.geometry("900x500")
            
            tk.Label(f_his, text="LỊCH SỬ SỬ DỤNG MÁY TÍNH", font=("Arial", 14, "bold"), pady=10).pack()

            frame = tk.Frame(f_his)
            frame.pack(fill="both", expand=True, padx=10, pady=5)
        
            scroll = tk.Scrollbar(frame)
            scroll.pack(side="right", fill="y")
        
            columns = ("ma_may", "tai_khoan", "luc_mo", "luc_tat", "tong_choi")
            tr_his = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scroll.set)
            

            tr_his.heading("ma_may", text="Mã Máy")
            tr_his.heading("tai_khoan", text="Tài Khoản")
            tr_his.heading("luc_mo", text="Giờ Mở")
            tr_his.heading("luc_tat", text="Giờ Tắt")
            tr_his.heading("tong_choi", text="Tổng Chơi (Giờ)")
        
            tr_his.column("ma_may", width=80, anchor="center")
            tr_his.column("tai_khoan", width=120, anchor="center")
            tr_his.column("luc_mo", width=180, anchor="center")
            tr_his.column("luc_tat", width=180, anchor="center")
            tr_his.column("tong_choi", width=120, anchor="center")
        
            tr_his.pack(fill="both", expand=True)
            scroll.config(command=tr_his.yview)
        
            try:
                with open("./json/lichsuchoi/lich_su_choi.json",'r',encoding="utf-8") as f:
                    data=json.load(f)
            except FileNotFoundError:
                messagebox.showerror("Lỗi", "Không tìm thấy file 3json!")

            for item in reversed(data):
                tr_his.insert("", "end", values=(
                    item.get("ma_may"),
                    item.get("tai_khoan"),
                    item.get("luc_mo_may"),
                    item.get("luc_tat_may"),
                    item.get("thoi_gian_DV_choi")
                ))
        
            btn_frame = tk.Frame(f_his)
            btn_frame.pack(pady=10)
        
            def xoalichsu():
                if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa vĩnh viễn toàn bộ lịch sử?"):
                    file_path = "./json/lichsuchoi/lich_su_choi.json"
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump([], f)
                    tr_his.delete(*tr_his.get_children())
                    messagebox.showinfo("Thông báo", "Đã xóa sạch lịch sử.")
        
            tk.Button(btn_frame, text="XÓA LỊCH SỬ", command=xoalichsu, bg="#e74c3c", fg="white").pack(side="left", padx=10)
            tk.Button(btn_frame, text="ĐÓNG", command=f_his.destroy, bg="#95a5a6", fg="white").pack(side="left", padx=10)
        
        def tru_gio():
            for ma_may, phien in list(phien_may.items()):
                phien["gio"] -= 1/60  
        
                if phien["gio"] <= 0:

                    tatmay(ma_may) 
                    messagebox.showinfo("Hết giờ", f"Máy {ma_may} đã hết giờ và tự tắt!")
            
            capnhat(dsmt.list)
            if smt.winfo_exists():
                smt.after(1000, tru_gio)
    
        def capnhat(ds):
            dsmt.sap_xep_ma_tang()
            tr.delete(*tr.get_children())
            for m in ds:
                ma = m.ma_may
                phien = phien_may.get(ma, {})
                gio = phien.get("gio", "")
                if gio != "":
                    gio = f"{round(gio, 2)} giờ"
    
                tr.insert("", "end", values=(
                    ma,
                    m.loai_may,
                    m.trang_thai,
                    phien.get("tai_khoan", "---"),
                    gio
                ))




        smt=tk.Toplevel() 
        smt.title("DVnh sách máy tính")
        smt.geometry("840x480")
        smt.configure(bg="#808080")
        
        frtc = tk.LabelFrame(smt, text="Tùy Chọn", bg="#808080", fg="white", font=("Arial", 10, "bold"))
        frtc.place(x=5, y=2, width=830, height=120)
        
        ictc = Image.open("./img/powerbutton.png")
        ictc= ictc.resize((64, 64), Image.LANCZOS)
        ictc = ImageTk.PhotoImage(ictc)

        btn_tc = tk.Button(
           smt,
           image=ictc,
           text="Mở Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
           command=momay
        )
        btn_tc.image = ictc
        btn_tc.place(x=10,y=20)

        ictc = Image.open("./img/poweron.png")
        ictc= ictc.resize((64, 64), Image.LANCZOS)
        ictc = ImageTk.PhotoImage(ictc)

        btn_tc = tk.Button(
           smt,
           image=ictc,
           text="Tắt Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
           command=tatmay_click
        )
        btn_tc.image = ictc
        btn_tc.place(x=90,y=20)

        ictc = Image.open("./img/search.png")
        ictc= ictc.resize((64, 64), Image.LANCZOS)
        ictc = ImageTk.PhotoImage(ictc)

        btn_tc = tk.Button(
           smt,
           image=ictc,
           text="Tìm Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
           command=timmay
        )
        btn_tc.image = ictc
        btn_tc.place(x=170,y=20)

        ictc = Image.open("./img/clock.png")
        ictc= ictc.resize((64, 64), Image.LANCZOS)
        ictc = ImageTk.PhotoImage(ictc)

        btn_tc = tk.Button(
           smt,
           image=ictc,
           text="Lịch Sử",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
           command=xemlichsu
        )
        btn_tc.image = ictc
        btn_tc.place(x=260,y=20)
        
        ictc = Image.open("./img/add.png")
        ictc= ictc.resize((64, 64), Image.LANCZOS)
        ictc = ImageTk.PhotoImage(ictc)

        btn_tc = tk.Button(
           smt,
           image=ictc,
           text="Thêm Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
           command=themmay
        )
        btn_tc.image = ictc
        btn_tc.place(x=350,y=20)
        
        ictc = Image.open("./img/rubbishbin.png")
        ictc= ictc.resize((64, 64), Image.LANCZOS)
        ictc = ImageTk.PhotoImage(ictc)

        btn_tc = tk.Button(
           smt,
           image=ictc,
           text="Xóa Máy",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
           command=xoamay
        )
        btn_tc.image = ictc
        btn_tc.place(x=440,y=20)
        
        ictc = Image.open("./img/settings.png")
        ictc= ictc.resize((64, 64), Image.LANCZOS)
        ictc = ImageTk.PhotoImage(ictc)

        btn_tc = tk.Button(
           smt,
           image=ictc,
           text="Sửa TTM",
           compound="top",
           bg="#808080",
           fg="white",
           bd=0,
           command=suamay
        )
        btn_tc.image = ictc
        btn_tc.place(x=530,y=20)

        frtr = tk.LabelFrame(smt, text="Thông tin máy tính", bg="#808080", fg="white", font=("Arial", 10, "bold"))
        frtr.place(x=2, y=130, width=830, height=400)

        tr = ttk.Treeview(smt, columns=("ma_may", "loai_may", "trang_thai", "ma_kh","thoi_gian_con_lai"), show="headings")
        tr.heading("ma_may", text="Mã máy")
        tr.heading("loai_may", text="Loại máy")
        tr.heading("trang_thai", text="Trạng thái")
        tr.heading("ma_kh", text="Tài khoản sử dụng")
        tr.heading("thoi_gian_con_lai", text="Thời gian")

        tr.place(x=10, y=150, width=810, height=320)

        tr.bind("<<TreeviewSelect>>")

        capnhat(dsmt.list)

        tru_gio()

        smt.mainloop()
    def dichvu():
        
        def xoaDV():
            selected = tr.selection()
            if not selected:
                messagebox.showwarning("Thông báo", "Vui lòng chọn một dịch vụ để xóa!")
                return

            val = tr.item(selected)['values']
            ma_dv = val[0]
            ten_dv = val[1]

            if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa dịch vụ: {ten_dv}?"):
                res, msg = dsdv.xoa(ma_dv)
                if res:
                    messagebox.showinfo("Thành công", msg)
                    capnhat(dsdv.list) 
                else:
                    messagebox.showerror("Lỗi", msg)
                
        def suaDV():
            selected = tr.selection()
            if not selected:
                messagebox.showwarning("Thông báo", "Vui lòng chọn dịch vụ cần sửa!")
                return

            val = tr.item(selected)['values']
            ma_cu = val[0]
            ten_cu = val[1]
            loai_cu = val[2]
            gia_cu = str(val[3]).replace(",", "") 
            sl_cu = val[4]

            f_sua = tk.Toplevel()
            f_sua.title(f"Sửa dịch vụ - {ma_cu}")
            f_sua.geometry("350x520")
            f_sua.grab_set()

            tk.Label(f_sua, text="Tên dịch vụ:").pack(pady=5)
            ent_ten = tk.Entry(f_sua); ent_ten.insert(0, ten_cu); ent_ten.pack()

            tk.Label(f_sua, text="Phân loại:").pack(pady=5)
            cb_loai = ttk.Combobox(f_sua, values=["đồ ăn", "nước uống", "thẻ game", "dịch vụ", "khác"], state="readonly")
            cb_loai.set(loai_cu); cb_loai.pack()

            tk.Label(f_sua, text="Giá bán:").pack(pady=5)
            ent_gia = tk.Entry(f_sua); ent_gia.insert(0, gia_cu); ent_gia.pack()

            tk.Label(f_sua, text="Số lượng tồn:").pack(pady=5)
            ent_sl = tk.Entry(f_sua); ent_sl.insert(0, sl_cu); ent_sl.pack()

            def xac_nhan():
                ten = " ".join(ent_ten.get().strip().title().split())
                loai = cb_loai.get()
                gia = ent_gia.get().strip()
                sl = ent_sl.get().strip()
                
                if not ten or not gia or not sl:
                    messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ các thông tin!")
                    return
                if not gia.isdigit() or not sl.isdigit():
                    messagebox.showerror("Lỗi", "Giá và Số lượng phải là số nguyên dương!")
                    return
                if int(gia) <= 0 or int(sl) <= 0:
                    messagebox.showerror("Lỗi", "Giá phải lớn hơn 0 và Số lượng không được âm!")
                    return
                dv_moi = DichVu(ma_cu, ten, int(gia), loai, int(sl))
                res, msg = dsdv.sua(dv_moi)
                if res:
                    messagebox.showinfo("Xong", "Đã cập nhật dịch vụ!")
                    f_sua.destroy()
                    capnhat(dsdv.list)
                else:
                    messagebox.showerror("Lỗi", msg)

            tk.Button(f_sua, text="CẬP NHẬT", bg="#f39c12", fg="white", font=("Arial", 10, "bold"), command=xac_nhan).pack(pady=30)
        def themDV():
            f_add = tk.Toplevel()
            f_add.title("Thêm Dịch Vụ / Hàng Hóa Mới")
            f_add.geometry("380x550")
            f_add.configure(bg="#f4f4f4")
            f_add.grab_set() 

            tk.Label(f_add, text="NHẬP THÔNG TIN DỊCH VỤ", font=("Arial", 12, "bold"), 
                    bg="#f4f4f4", fg="#2c3e50").pack(pady=20)

            fr_input = tk.Frame(f_add, bg="#f4f4f4")
            fr_input.pack(padx=20, fill="x")

            def input(label_text):
                tk.Label(fr_input, text=label_text, font=("Arial", 10), bg="#f4f4f4").pack(anchor="w", pady=(10, 0))
                entry = tk.Entry(fr_input, font=("Arial", 10), bd=1, relief="solid")
                entry.pack(fill="x", ipady=5)
                return entry

            ent_ma = input("Mã dịch vụ (ví dụ: DV001, DA001):")
            ent_ten = input("Tên dịch vụ / sản phẩm:")

            tk.Label(fr_input, text="Phân loại dịch vụ:", font=("Arial", 10), bg="#f4f4f4").pack(anchor="w", pady=(10, 0))
            cb_loai = ttk.Combobox(fr_input, values=["đồ ăn", "nước uống", "thẻ game", "dịch vụ", "khác"], state="readonly", font=("Arial", 10))
            cb_loai.current(0) 
            cb_loai.pack(fill="x", ipady=5)

            ent_gia = input("Giá bán (VNĐ):")
            ent_sl = input("Số lượng nhập kho:")

            def xnthem():
                ma = ent_ma.get().strip().upper()
                ten = " ".join(ent_ten.get().strip().title().split())
                loai = cb_loai.get()
                gia = ent_gia.get().strip()
                sl = ent_sl.get().strip()

                if not ma or not ten or not gia or not sl:
                    messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ các thông tin!")
                    return

                if not gia.isdigit() or not sl.isdigit():
                    messagebox.showerror("Lỗi", "Giá và Số lượng phải là số nguyên dương!")
                    return
                if int(gia) <= 0 or int(sl) < 0:
                    messagebox.showerror("Lỗi", "Giá phải lớn hơn 0 và Số lượng không được âm!")
                    return
                
                if not re.match(r"^(DV)\d{3}$", ma):
                    messagebox.showerror("Lỗi định dạng", "Mã dịch vụ phải bắt đầu bằng DV và theo sau bởi 3 chữ số!\nVí dụ: DV001, DV123")
                    return
                
                moi = DichVu(ma, ten, int(gia), loai, int(sl))
                
                success, msg = dsdv.them(moi) 
                
                if success:
                    messagebox.showinfo("Thành công", f"Đã thêm: {ten}")
                    f_add.destroy()

                    capnhat(dsdv.list) 
                else:
                    messagebox.showerror("Lỗi hệ thống", msg)

            tk.Button(f_add, text="LƯU DỊCH VỤ", bg="#27ae60", fg="white", 
                    font=("Arial", 11, "bold"), bd=0, cursor="hand2",
                    command=xnthem).pack(pady=30, padx=20, fill="x")
        
        def banDV():
            selected = tr.selection()
            if not selected:
                messagebox.showwarning("Thông báo", "Vui lòng chọn một dịch vụ để bán!")
                return

            val = tr.item(selected)['values']
            ma_dv = val[0]
            ten_dv = val[1]
            gia_dv = int(str(val[3]).replace(",", ""))
            ton_kho = int(val[4])

            f_ban = tk.Toplevel()
            f_ban.title(f"Thanh toán: {ten_dv}")
            f_ban.geometry("350x400")
            f_ban.grab_set()

            tk.Label(f_ban, text="Mã Khách Hàng (KHxxx):", font=("Arial", 10)).pack(pady=10)
            ent_makh = tk.Entry(f_ban); ent_makh.pack()

            tk.Label(f_ban, text="Số lượng mua:", font=("Arial", 10)).pack(pady=10)
            ent_sl = tk.Entry(f_ban); ent_sl.insert(0, "1"); ent_sl.pack()

            def xac_nhan_thanh_toan():
                ma_kh = ent_makh.get().strip().upper()
                sl_mua = ent_sl.get().strip()

                if not sl_mua.isdigit():
                    messagebox.showerror("Lỗi", "Số lượng phải là số!")
                    return
                
                sl_mua = int(sl_mua)
                tong_tien = sl_mua * gia_dv

                khach = dskh.tim_theo_ma(ma_kh) 
                if not khach:
                    messagebox.showerror("Lỗi", f"Không tìm thấy khách hàng có mã: {ma_kh}")
                    return
                
                if khach.so_tien < tong_tien:
                    messagebox.showerror("Lỗi", f"Khách hàng không đủ tiền!\nCần: {tong_tien:,}đ\nHiện có: {khach.so_tien:,}đ")
                    return

                if sl_mua > ton_kho:
                    messagebox.showerror("Lỗi", "Số lượng tồn kho không đủ!")
                    return

    
                khach.so_tien -= tong_tien
                dskh.file.save_data() 

                dv_obj = dsdv.tim_theo_ma(ma_dv)
                dv_obj.so_luong_ton -= sl_mua
                dsdv.file.save_data()

                luu(ma_kh, ma_dv, ten_dv, sl_mua, tong_tien)

                messagebox.showinfo("Thành công", 
                    f"Thanh toán hoàn tất!\n"
                    f"Khách hàng: {khach.ten_khach}\n"
                    f"Số dư còn lại: {khach.so_tien:,} VNĐ")
                
                f_ban.destroy()
                capnhat(dsdv.list) 

            tk.Button(f_ban, text="XÁC NHẬN BÁN", bg="#27ae60", fg="white", 
                    font=("Arial", 10, "bold"), command=xac_nhan_thanh_toan).pack(pady=30)
        def luu(ma_kh, ma_dv, ten_dv, sl, tong_tien):
            file_path = "./json/lichsuban/lichsu_banhang.json"
            
            new_record = {
                "ma_nhan_vien": ma,
                "ma_khach_hang": ma_kh,
                "ma_dich_vu": ma_dv,
                "ten_dich_vu": ten_dv,
                "so_luong": sl,
                "tong_tien": tong_tien,
                "thoi_gian": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            try:
    
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = []


                data.append(new_record)

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    
            except Exception as e:
                print(f"Lỗi khi lưu lịch sử: {e}")
        
        def timDV():
            f_tim = tk.Toplevel()
            f_tim.title("Tìm kiếm Dịch vụ")
            f_tim.geometry("350x250")
            f_tim.configure(bg="#f4f4f4")
            f_tim.grab_set()

            tk.Label(f_tim, text="NHẬP THÔNG TIN TÌM KIẾM", font=("Arial", 10, "bold"), bg="#f4f4f4").pack(pady=15)

            ent_tu = tk.Entry(f_tim, font=("Arial", 10), width=30)
            ent_tu.pack(pady=5)
            ent_tu.focus_set()

            tk.Label(f_tim, text="Tìm kiếm theo:", bg="#f4f4f4").pack(pady=5)
            cb_tieuchi = ttk.Combobox(f_tim, values=["Mã dịch vụ", "Tên dịch vụ"], state="readonly")
            cb_tieuchi.current(1) 
            cb_tieuchi.pack(pady=5)

            def tim():
                tu = ent_tu.get().strip()
                tieuchi = cb_tieuchi.get()

                if not tu:
                    messagebox.showwarning("Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
                    return

                ket_qua = []

                if tieuchi == "Mã dịch vụ":

                    obj = dsdv.tim_theo_ma(tu)
                    if obj:
                        ket_qua = [obj]
                else:
         
                    ket_qua = dsdv.tim_theo_ten(tu)

                if ket_qua:
              
                    capnhat(ket_qua)
                    f_tim.destroy()
                else:
                    messagebox.showinfo("Kết quả", f"Không tìm thấy dịch vụ nào cho: '{tu}'")


            tk.Button(f_tim, text="TÌM KIẾM", bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                    width=15, command=tim).pack(pady=20)

            f_tim.bind('<Return>', lambda event: tim())
        
        def xemLichSu():
            f_ls = tk.Toplevel()
            f_ls.title("Lịch sử giao dịch dịch vụ")
            f_ls.geometry("900x500")
            f_ls.configure(bg="#f4f4f4")
            f_ls.grab_set()

            tk.Label(f_ls, text="LỊCH SỬ BÁN HÀNG & DỊCH VỤ", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#2c3e50").pack(pady=15)

            fr_table = tk.Frame(f_ls)
            fr_table.pack(padx=10, fill="both", expand=True)

            columns = ("tg", "makh", "madv", "tendv", "sl", "tong")
            tr_ls = ttk.Treeview(fr_table, columns=columns, show="headings")

            tr_ls.heading("tg", text="Thời Gian"); tr_ls.column("tg", width=150, anchor="center")
            tr_ls.heading("makh", text="Mã KH"); tr_ls.column("makh", width=80, anchor="center")
            tr_ls.heading("madv", text="Mã DV"); tr_ls.column("madv", width=80, anchor="center")
            tr_ls.heading("tendv", text="Tên Dịch Vụ"); tr_ls.column("tendv", width=200, anchor="w")
            tr_ls.heading("sl", text="SL"); tr_ls.column("sl", width=50, anchor="center")
            tr_ls.heading("tong", text="Tổng Tiền"); tr_ls.column("tong", width=120, anchor="e")

            tr_ls.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(fr_table, orient="vertical", command=tr_ls.yview)
            tr_ls.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            
            total_revenue = 0
            try:
                with open("lichsu_banhang.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
            
                    for item in reversed(data):
                        tr_ls.insert("", "end", values=(
                            item["thoi_gian"],
                            item["ma_khach_hang"],
                            item["ma_dich_vu"],
                            item["ten_dich_vu"],
                            item["so_luong"],
                            f"{item['tong_tien']:,} VNĐ"
                        ))
                        total_revenue += int(item["tong_tien"])
            except (FileNotFoundError, json.JSONDecodeError):
                messagebox.showinfo("Thông báo", "Chưa có lịch sử giao dịch nào!")

            lbl_revenue = tk.Label(f_ls, text=f"TỔNG DOANH THU: {total_revenue:,} VNĐ", 
                                font=("Arial", 12, "bold"), fg="#e74c3c", bg="#f4f4f4")
            lbl_revenue.pack(pady=15)

            tk.Button(f_ls, text="ĐÓNG", width=15, command=f_ls.destroy).pack(pady=5)
                                
        def capnhat(ds):
            tr.delete(*tr.get_children())
            for dd in ds:
                tr.insert("", "end", values=(
                    dd.ma_dd, 
                    dd.ten_dd, 
                    dd.loai,
                    dd.gia, 
                    dd.so_luong_ton
                ))

        sdv = tk.Toplevel()
        sdv.title("Hệ thống Quản lý Dịch vụ & Hàng hóa")
        sdv.geometry("840x550")
        sdv.configure(bg="#808080")
        sdv.grab_set()

        frtc = tk.LabelFrame(sdv, text="Bảng Điều Khiển", bg="#808080", fg="white", font=("Arial", 10, "bold"))
        frtc.place(x=5, y=2, width=830, height=120)

        def tao_icon(path):
            img = Image.open(path).resize((60, 60), Image.LANCZOS)
            return ImageTk.PhotoImage(img)

        ic_find = tao_icon("./img/sell.png")
        btn_find = tk.Button(sdv, image=ic_find, text="Bán", compound="top", bg="#808080", fg="white", bd=0, command=banDV)
        btn_find.image = ic_find; btn_find.place(x=10, y=20)

        ic_find = tao_icon("./img/find.png")
        btn_find = tk.Button(sdv, image=ic_find, text="Tìm Kiếm", compound="top", bg="#808080", fg="white", bd=0, command=timDV)
        btn_find.image = ic_find; btn_find.place(x=90, y=20)

        ic_all = tao_icon("./img/filter.png")
        btn_all = tk.Button(sdv, image=ic_all, text="Tất Cả", compound="top", bg="#808080", fg="white", bd=0, command=lambda: capnhat(dsdv.list))
        btn_all.image = ic_all; btn_all.place(x=170, y=20)

        ic_all = tao_icon("./img/clock.png")
        btn_all = tk.Button(sdv, image=ic_all, text="Lịch sữ", compound="top", bg="#808080", fg="white", bd=0, command=xemLichSu)
        btn_all.image = ic_all; btn_all.place(x=260, y=20)
        
        ic_add = tao_icon("./img/plus.png")
        btn_add = tk.Button(sdv, image=ic_add, text="Thêm DV", compound="top", bg="#808080", fg="white", bd=0, command=themDV)
        btn_add.image = ic_add; btn_add.place(x=350, y=20)

        ic_fix = tao_icon("./img/mechanic.png")
        btn_fix = tk.Button(sdv, image=ic_fix, text="Sửa DV", compound="top", bg="#808080", fg="white", bd=0, command=suaDV)
        btn_fix.image = ic_fix; btn_fix.place(x=440, y=20)

  
        ic_del = tao_icon("./img/recycle-bin.png")
        btn_del = tk.Button(sdv, image=ic_del, text="Xóa DV", compound="top", bg="#808080", fg="white", bd=0, command=xoaDV)
        btn_del.image = ic_del; btn_del.place(x=530, y=20)
        
        

        frtr = tk.LabelFrame(sdv, text="Danh Mục Dịch vụ Hiện Có", bg="#808080", fg="white", font=("Arial", 10, "bold"))
        frtr.place(x=5, y=130, width=830, height=410)

        tr = ttk.Treeview(frtr, columns=("ma", "ten", "loai", "gia", "sl"), show="headings")
        
        tr.heading("ma", text="Mã Dịch Vụ"); tr.column("ma", width=100, anchor="center")
        tr.heading("ten", text="Tên Dịch Vụ / Sản Phẩm"); tr.column("ten", width=250, anchor="w")
        tr.heading("loai", text="Phân Loại"); tr.column("loai", width=120, anchor="center")
        tr.heading("gia", text="Đơn Giá (VNĐ)"); tr.column("gia", width=120, anchor="e")
        tr.heading("sl", text="Số Lượng Tồn"); tr.column("sl", width=100, anchor="center")

        tr.pack(fill="both", expand=True, padx=5, pady=5)
        
        capnhat(dsdv.list)
        
        sdv.mainloop()
    def thongKeAdmin():

            if vt != "quản trị":
                messagebox.showerror("Từ chối", "Chức năng này chỉ dành cho Quản trị viên!")
                return

            f_tk = tk.Toplevel()
            f_tk.title("Hệ Thống Thống Kê Tài Chính Quản Trị")
            f_tk.geometry("1000x700")
            f_tk.configure(bg="#1a1a1a")
            f_tk.grab_set()


            

            tong_luong = sum(int(getattr(nv, "luong", 0)) for nv in dsnv.list)

   
            tong_tien_khach = sum(int(getattr(kh, "so_tien", 0)) for kh in dskh.list)


            tong_doanh_thu = 0
            so_don_hang = 0
            try:
                with open("lichsu_banhang.json", "r", encoding="utf-8") as f:
                    ls_data = json.load(f)
                    so_don_hang = len(ls_data)
                    tong_doanh_thu = sum(int(item["tong_tien"]) for item in ls_data)
            except:
                ls_data = []


            tk.Label(f_tk, text="BÁO CÁO TÀI CHÍNH TỔNG QUÁT", font=("Arial", 20, "bold"), 
                    fg="#f1c40f", bg="#1a1a1a").pack(pady=30)

  
            fr_cards = tk.Frame(f_tk, bg="#1a1a1a")
            fr_cards.pack(fill="x", padx=40)

            def draw_card(parent, title, value, color, subtitle=""):
                card = tk.Frame(parent, bg="#2d3436", highlightthickness=2, highlightbackground=color, padx=20, pady=25)
                card.pack(side="left", padx=15, expand=True, fill="both")
                
                tk.Label(card, text=title, font=("Arial", 11), fg="white", bg="#2d3436").pack()
                tk.Label(card, text=value, font=("Arial", 16, "bold"), fg=color, bg="#2d3436").pack(pady=10)
                if subtitle:
                    tk.Label(card, text=subtitle, font=("Arial", 9, "italic"), fg="#b2bec3", bg="#2d3436").pack()

    
            draw_card(fr_cards, "DOANH THU DỊCH VỤ", f"{tong_doanh_thu:,} đ", "#2ecc71", f"Tổng cộng {so_don_hang} đơn hàng")
            

            draw_card(fr_cards, "TIỀN TRONG TÀI KHOẢN KH", f"{tong_tien_khach:,} đ", "#3498db", f"Số dư của {len(dskh.list)} khách")
            

            draw_card(fr_cards, "TỔNG QUỸ LƯƠNG NV", f"{tong_luong:,} đ", "#e74c3c", f"Dự chi cho {len(dsnv.list)} nhân viên")

            lbl_detail = tk.Label(f_tk, text="CHI TIẾT LỊCH SỬ GIAO DỊCH GẦN ĐÂY", 
                                font=("Arial", 12, "bold"), fg="white", bg="#1a1a1a")
            lbl_detail.pack(pady=(40, 10))

            fr_table = tk.Frame(f_tk)
            fr_table.pack(padx=40, fill="both", expand=True)

            columns = ("tg", "makh", "tendv", "sl", "tong")
            tr_ls = ttk.Treeview(fr_table, columns=columns, show="headings", height=8)
            
            tr_ls.heading("tg", text="Thời Gian"); tr_ls.column("tg", width=180, anchor="center")
            tr_ls.heading("makh", text="Mã Khách"); tr_ls.column("makh", width=100, anchor="center")
            tr_ls.heading("tendv", text="Sản Phẩm/Dịch Vụ"); tr_ls.column("tendv", width=250)
            tr_ls.heading("sl", text="SL"); tr_ls.column("sl", width=70, anchor="center")
            tr_ls.heading("tong", text="Thành Tiền"); tr_ls.column("tong", width=150, anchor="e")

            
            for item in reversed(ls_data[-20:]):
                tr_ls.insert("", "end", values=(item["thoi_gian"], item["ma_khach_hang"], 
                                            item["ten_dich_vu"], item["so_luong"], f"{item['tong_tien']:,} đ"))
            
            tr_ls.pack(side="left", fill="both", expand=True)
            
            sc = ttk.Scrollbar(fr_table, orient="vertical", command=tr_ls.yview)
            tr_ls.configure(yscroll=sc.set)
            sc.pack(side="right", fill="y")

            tk.Button(f_tk, text="ĐÓNG BÁO CÁO", font=("Arial", 10, "bold"), width=20,
                    bg="#636e72", fg="white", command=f_tk.destroy).pack(pady=20)
    
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


    icdd = Image.open("./img/customer-service.png")
    icdd= icdd.resize((64, 64), Image.LANCZOS)
    icdd = ImageTk.PhotoImage(icdd)

    btn_dd = tk.Button(
        s1,
        image=icdd,
        text="Dịch vụ",
        compound="top",
        bg="#1e1e1e",
        fg="white",
        bd=0,
        command=dichvu
    )
    btn_dd.image = icdd
    btn_dd.place(x=50, y=350)
    
    
    ictk = Image.open("./img/analytics.png")
    ictk= ictk.resize((64, 64), Image.LANCZOS)
    ictk = ImageTk.PhotoImage(ictk)
    btn_tk   = tk.Button(
        s1,
        image=ictk,
        text="Thống kê",
        compound="top",
        bg="#1e1e1e",
        fg="white",
        bd=0,
        command=thongKeAdmin
    )
    btn_tk.image = ictk
    btn_tk.place(x=50, y=450)

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
    print(ds)
    ten=enten.get()
    mk=enmk.get()
    manv=None
    vt=None
    dk=False
    if ten=="" or mk=="":
        messagebox.showerror("Lỗi","Tên và Mật khẩu không để trống!!!")
        enmk.delete(0, tk.END)
    else:
        for nv in ds:
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
    with open("./json/nhan_vien.json",'r',encoding="utf-8") as f:
        ds=json.load(f)
except FileNotFoundError:
    messagebox.showerror("Lỗi", "Không tìm thấy file 3json!")

s.mainloop()