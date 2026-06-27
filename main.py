import os
from ctypes import CDLL, c_bool, c_int
import traceback
def erro(word):
    print("Erro:\n",word)
i=0
type_shuju=0
side=""
try:
    base_path =os.path.dirname(os.path.realpath(__file__))
    dll_address=os.path.join(base_path,"backend.dll")
    c=CDLL(dll_address)
    c.number_size.restype = c_bool
    c.number.restype = c_int
except Exception:
    erro(traceback.format_exc())
while type_shuju not in ["B","KB","MB","GB"]:
    type_shuju = str(input("输入生成的单位(B,KB,MB,GB):")).strip().upper()
while True:
    try:
        side=int(input("生成的大小:"))
        shuju_size=c.number_size(side, type_shuju.encode("utf-8"))
        if shuju_size :
            break
        else: print("你输入为负数或太大,请重新输入")
    except ValueError:
        erro("请输入整数!")
def panduan(y_n):
    if y_n == 0:
        print("ok")
    elif y_n == 1:
        erro("文件创建失败")  
    elif y_n == 2:
        erro("文件写入失败")
    elif y_n == 3:
        erro("获取路径失败")
    elif y_n == 4:
        erro("单位非法")
    elif y_n == 5:
        erro("数值溢出")
    else:
        erro("未知错误")
y_n=c.number(side,type_shuju.encode('utf-8'))
panduan(y_n)