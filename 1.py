import tkinter as tk
from tkinter import messagebox
win=tk.Tk()
win.title("储存生成工具")
win.geometry("400x300")
win.resizable(width=False, height=False)

type_Checkbox=tk.StringVar()
type_Checkbox.set("B")
type_list=["B","KB","MB","GB"]
type_box=tk.OptionMenu(win,type_Checkbox,*type_list)
type_label = tk.Label(win, text="生成文件类型:", font=("宋体",12))
type_label.place(x=0,y=0)

win.mainloop()