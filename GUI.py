import tkinter as tk
from threading import Thread
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
import uuid

win=tk.Tk()
win.title("储存生成工具")
win.geometry("400x300")
win.resizable(width=False, height=False)
panduan_bool=True

def address_get():
    address_path=filedialog.askdirectory(title="文件储存路径选择",initialdir = "C:/")
    if address_path:
        address_Entry.config(state="normal")
        address_Entry.delete(0,tk.END)
        address_Entry.insert(0,address_path)
        address_Entry.config(state="readonly")
        path_long =len(address_path)
        if path_long<=25:
            address_Entry.config(width=path_long + 3)
        else:
            address_Entry.config(width=28)

def shuju_panduan():
    global panduan_bool
    if not panduan_bool:
        return
    panduan_bool = False
    address_Entry.config(state="normal")
    check_address = address_Entry.get()
    address_Entry.config(state="readonly")
    check_num_bool,check_num_erro=check_num()
    if not check_num_bool:
        panduan_bool=True
        messagebox.showerror("错误", check_num_erro)
        return
    check=Thread(target=check_quanxian,args=(win,check_address),daemon=True)
    check.start()
def check_num():
    check_text=wold_shuju_entry.get()
    if check_text=="":
        #messagebox.showerror("错误", "文件大小不能为空")
        return False,"文件大小不能为空"
    if not check_text.isdigit():
        #messagebox.showerror("错误", "生成大小只能输入数字")
        wold_shuju_entry.delete(0,tk.END)
        wold_shuju_entry.insert(0,"")
        return False,"生成大小只能输入数字"
    return True,""

def check_quanxian(win,check_address):
    if check_address=="":
        win.after(0,shuju_result,False,"路径不能为空")
        return
    if not os.path.isdir(check_address) or not os.path.exists(check_address):
        print("路径不是有效文件夹")
        #messagebox.showerror("错误", "路径不是有效文件夹")
        win.after(0,shuju_result,False,"路径不是有效文件夹")
        return
    temporary_name = f"_perm_test_{uuid.uuid4().hex}"
    temporary_name = os.path.join(check_address, temporary_name)
    try:
        print("ok")
        with open(temporary_name,"x"):
            pass
        print("oo")
        win.after(0,shuju_result,True,"")
        return
    except PermissionError:
        print("权限不足")
        #messagebox.showerror("错误", "权限不足")
        win.after(0, shuju_result, False, "权限不足")
        return
    except OSError:
        print("目录被锁定了或该磁盘为只读磁盘或磁盘已满")
        #messagebox.showerror("错误", "目录被锁定了或该磁盘为只读磁盘或磁盘已满")
        win.after(0,shuju_result,False,"目录被锁定了或该磁盘为只读磁盘或磁盘已满")
        return
    except Exception:
        print("未知错误")
        #messagebox.showerror("错误","未知错误")
        win.after(0,shuju_result,False,"未知错误")
        return
    finally:
        if os.path.exists(temporary_name):
            os.remove(temporary_name)

def shuju_result(check_result,result_text):
    global panduan_bool
    if not check_result:
        messagebox.showerror("错误", result_text)
        panduan_bool=True
        return
    type_shuju_get = type_xuan.get()
    wold_shuju_get = wold_shuju_entry.get()
    address_shuju_get = address_Entry.get()
    print("--")
    print(type_shuju_get)
    print(wold_shuju_get)
    print(address_shuju_get)
    print("__")
    panduan_bool=True
    return

type_frame=tk.Frame(win)
type_under_kuang_xuan=tk.StringVar(value="MB")
type_under_kuang_list=["B","KB","MB","GB"]
type_xuan=ttk.Combobox(
    type_frame,
    textvariable=type_under_kuang_xuan,
    values=type_under_kuang_list,
    state="readonly",
    width=8
)
type_label = tk.Label(type_frame, text="生成单位:", font=("黑体",12))
type_xuan.grid(column=1, row=0, padx=0, pady=0)
type_label.grid(column=0, row=0, padx=0, pady=0)

wold_shuju=tk.Frame(win)
wold_shuju_label=tk.Label(wold_shuju,text="生成大小:",font=("黑体",12))
wold_shuju_entry=tk.Entry(wold_shuju,width=10,)
wold_shuju_label.grid(column=0, row=0, padx=0,pady=5)
wold_shuju_entry.grid(column=1, row=0, padx=0, pady=5)
#wold_shuju_entry.bind("<FocusOut>",check_num)

address_shuju=tk.Frame(win)
address_Label_tip=tk.Label(address_shuju,text="文件存放路径:",font=("黑体",12))
address_Entry=tk.Entry(address_shuju,state="readonly",width=10,font=("黑体",12))
address_Button=tk.Button(address_shuju,text="选择地址",command=address_get)
address_Label_tip.grid(column=0, row=0, padx=0, pady=0)
address_Entry.grid(column=1, row=0, padx=0, pady=5)
address_Button.grid(column=2, row=0, padx=0, pady=0)

bottom=tk.Button(win,text="开始生成",font=("黑体",12),command=shuju_panduan)
bottom.grid(column=0,row=3,sticky="",columnspan=3)

type_frame.grid(column=0, row=0, padx=0, pady=0,sticky="w")
wold_shuju.grid(column=0, row=1, padx=0, pady=0,sticky="w")
address_shuju.grid(column=0, row=2, padx=0, pady=0,sticky="w")

win.mainloop()