import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog
import json
import os

class KhachHang:
    def __init__(self,ma_khach,ten_khach,so_dien_thoai,tai_khoan,mat_khau,so_tien,gio_choi):
        self.ma_khach = ma_khach
        self.ten_khach = ten_khach
        self.so_dien_thoai = so_dien_thoai
        self.tai_khoan = tai_khoan
        self.mat_khau = mat_khau
        self.so_tien = so_tien
        self.gio_choi = gio_choi

    def to_dict(self):
        return {"ma_khach":self.ma_khach,"ten_khach":self.ten_khach,"so_dien_thoai":self.so_dien_thoai,
                "tai_khoan":self.tai_khoan,"mat_khau":self.mat_khau,"so_tien":self.so_tien,"gio_choi":self.gio_choi}

class QuanLyKhachHang:
    def __init__(self,filename = "khach_hang.json"):
        self.list_kh = []
        self.filename = filename
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename,"r",encoding = "utf-8") as file:
                data = json.load(file)
                self.list_kh = []
                for item in data:
                    kh = KhachHang(item["ma_khach"],item["ten_khach"],item["so_dien_thoai"],
                                   item["tai_khoan"],item["mat_khau"],item["so_tien"],item["gio_choi"])
                    self.list_kh.append(kh)
        else:
            self.list_kh = [KhachHang("KH001","Nguyễn Văn A","0901234567","nguyenvana","123456",200000,10),
                            KhachHang("KH002","Trần Văn B","0902345678","tranvanb","123456",150000,7.5)]
            self.save_data()

    def save_data(self):
        data = [kh.to_dict() for kh in self.list_kh]
        with open(self.filename,"w",encoding = "utf-8") as file:
            json.dump(data,file,ensure_ascii = False,indent = 4)

    def them_kh(self,khach_hang):
        ma_kh = khach_hang.ma_khach.strip().upper()
        for kh in self.list_kh:
            if ma_kh == kh.ma_khach.strip().upper():
                return False,f"Mã khách '{ma_kh}' đã tồn tại!"
        self.list_kh.append(khach_hang)
        self.save_data()
        return True,f"Thêm khách hàng thành công!"

    def update_kh (self,khach_hang):
        ma_kh = khach_hang.ma_khach.strip().upper()
        for i,kh in enumerate(self.list_kh):
            if ma_kh == kh.ma_khach.strip().upper():
                self.list_kh[i]= khach_hang
                self.save_data()
                return True,f"Cập nhật khách hàng thành công!"
        return False,f"Mã khách '{ma_kh}' không tồn tại!"

    def xoa_kh(self,khach_hang):
        ma_kh = khach_hang.ma_khach.strip().upper()
        for kh in self.list_kh:
            if ma_kh == kh.ma_khach.strip().upper():
                self.list_kh.remove(kh)
                return True,f"Xóa khách hàng thành công!"
        return False,f"Mã khách '{ma_kh}' không tồn tại!"

class NhanVien:
    def __init__(self,ma_nhan_vien,ten_nhan_vien,ten_dang_nhap,mat_khau,vai_tro):
        self.ma_nv = ma_nhan_vien
        self.ten_nv = ten_nhan_vien
        self.ten_dn = ten_dang_nhap
        self.mat_khau = mat_khau
        self.vai_tro = vai_tro

    def to_dict(self):
        return {"ma_nhan_vien":self.ma_nv,"ten_nhan_vien":self.ten_nv,
                "ten_dang_nhap":self.ten_dn,"mat_khau":self.mat_khau,"vai_tro":self.vai_tro}

class DSNV:
    def __init__(self,filename = "nhan_vien.json"):
        self.list_nv = []
        self.filename = filename
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename,"r",encoding = "utf-8") as file:
                data = json.load(file)
                self.list_nv = []
                for item in data:
                    nv = NhanVien(item["ma_nhan_vien"],item["ten_nhan_vien"],item["ten_dang_nhap"],
                                   item["mat_khau"],item["vai_tro"])
                    self.list_nv.append(nv)
        else:
            self.list_nv = [NhanVien("NV001","Admin","admin","123456","quản trị")]
            self.save_data()

    def save_data(self):
        data = [nv.to_dict() for nv in self.list_nv]
        with open(self.filename,"w",encoding = "utf-8") as file:
            json.dump(data,file,ensure_ascii = False,indent = 4)

    def them_nv(self,nhan_vien):
        ma_nv = nhan_vien.ma_nv.strip().upper()
        for nv in self.list_nv:
            if ma_nv == nv.ma_nv.strip().upper():
                return False,f"Mã nhân viên '{ma_nv}' đã tồn tại!"
        self.list_nv.append(nhan_vien)
        self.save_data()
        return True,f"Thêm nhân viên thành công!"

    def update_nv (self,nhan_vien):
        ma_nv = nhan_vien.ma_nv.strip().upper()
        for i,nv in enumerate(self.list_nv):
            if ma_nv == nv.ma_nv.strip().upper():
                self.list_nv[i]= nhan_vien
                self.save_data()
                return True,f"Cập nhật nhân viên thành công!"
        return False,f"Mã nhân viên '{ma_nv}' không tồn tại!"

    def xoa_nv(self,nhan_vien):
        ma_nv = nhan_vien.ma_nv.strip().upper()
        for nv in self.list_nv:
            if ma_nv == nv.ma_nv.strip().upper():
                self.list_nv.remove(nv)
                self.save_data()
                return True,f"Xóa nhân viên thành công!"
        return False,f"Mã nhân viên '{ma_nv}' không tồn tại!"



def luu(n,ds):
    with open("n", "w", encoding="utf-8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=4)  

phien_may = {}       
def formmain(ma,vt):
    
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
