import tkinter as tk
from pydoc import text
from tkinter import messagebox, font
from tkinter import ttk

import select

win=tk.Tk()
win.title("储存生成工具")
win.geometry("400x300")
win.resizable(width=False, height=False)

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

wold_shuru=tk.Frame(win)
wold_shuru_label=tk.Label(wold_shuru,text="生成大小:",font=("黑体",12))
wold_shuru_entry=tk.Entry(wold_shuru,width=10)
wold_shuru_label.grid(column=0, row=0, padx=0)
wold_shuru_entry.grid(column=1, row=0, padx=0, pady=5)

bottom=tk.Button(win,text="开始生成",font=("黑体",12))

type_frame.grid(column=0, row=0, padx=0, pady=0,sticky="w")
wold_shuru.grid(column=0, row=1, padx=0, pady=0)
win.mainloop()