#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:赵杭天

import tkinter as tk
from tkinter import messagebox
import numpy as np

window = tk.Tk()
window.title('幻方 v0.1  -- by ZHT')
window.iconbitmap('icon.ico')
window.geometry('500x300')  # 这里的乘是小x


frame = tk.Frame(window)
frame.grid(row=0, column=0)

frame_up = tk.Frame(frame)
frame_bottom = tk.Frame(frame)
frame_up.pack(side='top')
frame_bottom.pack(side='bottom')

frame_head = tk.Frame(frame_up)
frame_head.grid(row=0, column=0)
frame_u = tk.Frame(frame_head)
frame_m = tk.Frame(frame_head)
frame_u.pack(side='top')
frame_m.pack(side='bottom')

text1 = tk.Label(frame_u, text='幻方阶数：', width=12, height=2)
text1.grid(row=0, column=0)
entry = tk.Entry(frame_u, show=None)  # 显示成明文形式
entry.insert(0, '3')
entry.grid(row=0, column=1)
labelText = tk.StringVar()
text2 = tk.Label(frame_u, textvariable=labelText, width=30, height=2)
labelText.set("幻方状态：")
text2.grid(row=0, column=2)


# 幻方验证函数
def valid(matrix, order):
    """
    检验矩阵是否满足全对称幻方的要求
    :param matrix:
    :return: 0 or 1 or 2 (no ms, ms, perfect ms)
    """
    ms_type = 0
    # 阶数小于3不存在幻方
    if matrix.shape[0] <= 2:
        return 0
    # 检查是否使用了重复的数
    use_num = []
    for i in range(0, order):
        for j in range(0, order):
            if matrix[i, j] in use_num:
                return ms_type
            else:
                use_num.append(matrix[i, j])

    equal_sum = sum(matrix[0, :])
    # 列和相等
    for i in range(1, order):
        if not sum(matrix[i, :]) == equal_sum:
            return ms_type
    # 行和相等
    for j in range(0, order):
        if not sum(matrix[:, j]) == equal_sum:
            return ms_type
    # 主对角线和相等
    dig_sum = 0
    for i in range(0, order):
        dig_sum += matrix[i, i]
    if not dig_sum == equal_sum:
        return ms_type
    # 副对角线和相等
    dig_sum = 0
    for i in range(0, order):
        dig_sum += matrix[i, order - 1 - i]
    if not dig_sum == equal_sum:
        return ms_type

    ms_type = 1  # 进行到这里，已知道该矩阵属于幻方

    # 检查泛对角线  n阶幻方有2n条泛对角线(n>2)
    # 先生成索引，再根据索引计算
    n = order
    indexes = []
    for i in range(1, n):  # 不再重复计算主对角线
        tmp = [[(i + t) % n, t] for t in range(0, n)]
        indexes.append(tmp)
    for i in range(1, n):  # 不再重复计算副对角线
        tmp = [[(i + n - t) % n, t] for t in range(0, n)]
        indexes.append(tmp)
    for gd in indexes:
        generalized_dig_sum = 0
        for p in gd:
            generalized_dig_sum += matrix[p[0], p[1]]
        if not generalized_dig_sum == equal_sum:
            return ms_type

    ms_type = 2  # 进行到这里，已知道该矩阵属于完美幻方
    return ms_type


# 触发按钮点击事件的函数
def make_empty():
    for widget in frame_bottom.winfo_children():
        widget.destroy()
    order = int(entry.get())
    print('make_empty')
    labelText.set("幻方状态：非幻方")
    text2.config(fg='black')
    for i in range(2, 2 + order):  # 从第二行开始绘制表格
        for j in range(order):
            tmp = tk.Entry(frame_bottom, text='', width=3).grid(row=i, column=j, padx=5, pady=5, ipadx=5, ipady=5)


def valid_ms():
    order = int(entry.get())
    print('valid_ms')
    matrix = np.zeros([order, order])
    if not frame_bottom.winfo_children():
        print('空幻方')
        labelText.set("幻方状态：空")
        return
    for i, widget in enumerate(frame_bottom.winfo_children()):
        if isinstance(i, str) or not str.isdigit(widget.get()):
            print(i, widget.get())
            print('非幻方')
            labelText.set("幻方状态：非幻方")
            return
        matrix[int(i / order)][i % order] = widget.get()
    print("输入矩阵：\n", matrix)
    ms_type = valid(matrix, order)
    if ms_type == 0:
        print('非幻方')
        labelText.set("幻方状态：非幻方")
    elif ms_type == 1:
        print('普通幻方')
        labelText.set("幻方状态：普通幻方")
        text2.config(fg='blue')
    elif ms_type == 2:
        print('完美幻方')
        labelText.set("幻方状态：完美幻方！")
        text2.config(fg='red')


def gen_ms():
    print('gen_ms')
    messagebox.showinfo(title='暂时还没实现 ╮(￣▽￣)╭', message='该功能将在后续版本中添加！')


def about_msg(event):
    print('about')
    messagebox.showinfo(title='关于本程序', message='《系辞》云：“河出图，洛出书，圣人则之。”\n'
                                               '本程序来源于李老师的一个提问，\n'
                                               '由于兴趣，便在一个下午完成了第一个版本，\n'
                                               '本程序的【普通幻方】即：\n'
                                               '满足行、列、主副对角线之和相等的矩阵\n'
                                               '本程序的【完美幻方】即：\n'
                                               '满足行、列、主对角线及泛对角线各数之和均相等的矩阵\n'
                                               '有兴趣的老师同学欢迎交流:\n'
                                               'jp-vip@qq.com 18级学生 赵杭天')


# 放置按钮
b1 = tk.Button(frame_m, text='重新输入', width=10, height=2, command=make_empty).grid(row=1, column=0)
b2 = tk.Button(frame_m, text='检验幻方', width=10, height=2, command=valid_ms).grid(row=1, column=1)
b3 = tk.Button(frame_m, text='生成幻方', width=10, height=2, command=gen_ms).grid(row=1, column=2)
about = tk.Label(frame_u, text='关于程序', width=10, height=2, fg='blue')
about.grid(row=1, column=3)
about.bind('<Button>', about_msg)
# 主窗口循环显示
window.mainloop()
