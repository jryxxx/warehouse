# !/usr/bin/python3
# _*_ coding: utf-8 _*_
# 
# @Date        : 2025/5/6 21:20
# @Author      : Ruiyang Jia
# @File        : test.py
# @Software    : PyCharm
# @Description : 测试 3D 绘图

import matplotlib.pyplot as plt


def draw_3d():
    """
    Draw a 3D box using bar3d
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x, y, z = 10, 15, 0
    dx, dy, dz = 5, 8, 3

    ax.bar3d(x, y, z, dx, dy, dz, color='skyblue', edgecolor='k', alpha=0.8)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title("3D Box (bar3d)")
    plt.show()


if __name__ == '__main__':
    draw_3d()
