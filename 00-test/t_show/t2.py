# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# pylab是matplotlib的一个子包
# import pylab as pl

# 生成一维数据
x = np.linspace(-1, 1, 20)
y = 2 * x + 2
y_ = x ** 2
print(x, y)


def show1():
    # 定义一个图像窗口  定义图像窗口编号,大小
    plt.figure(num=3, figsize=(8, 8))
    # 绘制点线图 定义图像上的点，曲线颜色，曲线宽度，曲线类型, 添加图例在右上角
    plt.plot(x, y, marker='o', color='red', linewidth=2.0, linestyle='--', label='linear line')
    plt.plot(x, y_, label='square line')
    plt.legend(loc='upper right')
    # 设置x y坐标轴范围
    plt.xlim((-2, 4))
    plt.ylim((-2, 4))
    # 设置x y坐标轴名称
    plt.xlabel('x')
    plt.ylabel('y')
    # 设置x y坐标轴刻度
    x_ticks = np.linspace(-1, 1, 5)
    y_ticks = np.linspace(-1, 3, 5)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    # 添加文本注释
    plt.text(-1, 1, r'text info', fontdict={'size': 16, 'color': 'r'})
    # 标题
    plt.title("A simple plot")
    # 显示图像
    plt.show()




def show2():
    global x, y
    # 生成标准正态分布的二维数组
    x = np.random.normal(0, 1, 20)
    y = np.random.normal(0, 1, 20)
    color = np.arctan2(y, x)
    # 绘制散点图  定义散点大小，颜色，透明度
    plt.scatter(x, y, s=75, c=color, alpha=.5)
    # 设置x y坐标轴范围
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    # 隐藏坐标轴
    # plt.xticks(())
    # plt.yticks(())
    # 显示图像
    plt.show()


def show3():
    global x
    # 生成柱状图的数据
    n = 10
    x = np.arange(n)
    y1 = (1 - x / float(n)) * np.random.uniform(0.5, 1.0, n)
    y2 = (1 - x / float(n)) * np.random.uniform(0.5, 1.0, n)
    # 绘制柱状图 定义柱体颜色，边框颜色
    plt.bar(x, +y1, facecolor='#9999ff', edgecolor='white')
    plt.bar(x, -y2, facecolor='#ff9999', edgecolor='white')
    # 设置x y坐标轴范围
    plt.xlim(-2, n)
    plt.ylim(-2, 2)
    # 隐藏坐标轴
    # plt.xticks(())
    # plt.yticks(())
    # 在柱体上方增加数值 定义文本框位置，横向居中对齐，纵向底部对齐
    for i, j in zip(x, y1):
        plt.text(i, j + 0.05, '%.2f' % j, ha='center', va='bottom')
    for i, j in zip(x, y2):
        plt.text(i, -j - 0.15, '%.2f' % j, ha='center', va='bottom')
    # 显示图像
    plt.show()


def show4():
    global x, y
    # 绘制多幅图
    # 产生测试数据
    x = np.arange(1, 10)
    y = x
    fig = plt.figure()
    plt.figure()
    plt.subplot(121)
    plt.plot(x, y, color='green', label='fig1')
    plt.legend()
    plt.subplot(122)
    plt.plot(x, y, color='red', label='fig2')
    plt.legend()
    plt.show()




show2()

