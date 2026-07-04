import tkinter as tk
from pydoc import text
from tkinter import messagebox, font
from tkinter import ttk

import select

win=tk.Tk()
win.title("储存生成工具")
win.geometry("400x300")
win.resizable(width=False, height=False)

def shuju_get():
    type_shuju=type_xuan.get()
    wold_shuju=wold_shuju_entry.get()
    print(type_shuju)
    print(wold_shuju)
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
type_xuan.grid(column=1, row=0, padx=0, pady=5)
type_label.grid(column=0, row=0, padx=0, pady=0)

wold_shuju=tk.Frame(win)
wold_shuju_label=tk.Label(wold_shuju,text="生成大小:",font=("黑体",12))
wold_shuju_entry=tk.Entry(wold_shuju,width=10)
wold_shuju_label.grid(column=0, row=0, padx=0)
wold_shuju_entry.grid(column=1, row=0, padx=0, pady=5)

bottom=tk.Button(win,text="开始生成",font=("黑体",12),command=shuju_get)
bottom.grid(column=0,row=2)

type_frame.grid(column=0, row=0, padx=0, pady=0,sticky="w")
wold_shuju.grid(column=0, row=1, padx=0, pady=0)
win.mainloop()