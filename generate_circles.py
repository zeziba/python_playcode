#!/usr/bin/env python

"""
    Created by cengen on 3/24/18.
"""

import tkinter as tk
from math import sin, cos
from random import randint
import asyncio
from time import sleep

pi = 3.1415926535897932384626433832795028841971693993751058209749445923

width = 800
height = 600

r = 2

inc = pi / 60

dt = 100

master = tk.Tk()
w = tk.Canvas(master, width=width, height=height)


def map_(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def draw(event, window, radius, r_inc=4, inc_=pi / 60):
    c_x = event.x
    c_y = event.y
    r_max = ((width // 2) - c_x) ** 2 + ((height // 2) - c_y) ** 2
    r_max /= 2

    inc_list = []
    ii = -pi
    while ii < pi:
        inc_list.append(ii)
        ii += inc_

    gen_delta = lambda ij, r_: (r_ * cos(ij),
                                r_ * sin(ij),
                                int(map_(ij, -pi, pi, 0, 255)),
                                int(map_(sin(map_(r_, 0, r_max, 0, 255)), -1, 1, 0, 255)),
                                int(map_(cos(r_), -1, 1, 0, 255)))

    def draw_point(window_, x_, y_, dx_, dy_, dz_):
        outline = "#{}{}{}"
        window_.create_rectangle((x_, y_, x_, y_),
                                 outline=outline.format("%02x" % dx_, "%02x" % dy_, "%02x" % dz_))

    while radius ** 2 < r_max:
        points = list(map(lambda i: gen_delta(i, radius), inc_list))
        list(map(lambda point:
                 draw_point(window_=window, x_=c_x+point[0],
                            y_=c_y+point[1], dx_=point[2], dy_=point[3], dz_=point[4]), points))

        radius += r_inc


if __name__ == "__main__":
    w.pack()

    w.bind("<Button-1>", lambda event: draw(event, w, randint(2, 12), randint(2, 7)), pi/randint(6, 250))
    master.protocol("WM_DELETE_WINDOW", exit)
    master.mainloop()
