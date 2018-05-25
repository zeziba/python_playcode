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

width = 1600
height = 1200

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

    def get_angle():
        ci = -pi
        while ci < pi:
            yield ci
            ci += inc_

    def get_radius():
        cr = radius / r_inc
        while cr < radius:
            yield cr
            cr += radius / r_inc

    def gen_point(theta, rad_):
        return rad_ * cos(theta), rad_ * sin(theta), int(map_(theta, -pi, pi, 0, 255)), \
               int(map_(sin(map_(rad_, 0, radius, 0, 255)), -1, 1, 0, 255)), int(map_(cos(rad_), -1, 1, 0, 255))

    def gen_circle():
        r__ = get_radius()
        for r_ in r__:
            ang_ = get_angle()
            for a_ in ang_:
                yield gen_point(a_, r_)

    def draw_point(window_, x_, y_, dx_, dy_, dz_):
        outline = "#{}{}{}"
        window_.create_rectangle((x_, y_, x_, y_),
                                 outline=outline.format("%02x" % dx_, "%02x" % dy_, "%02x" % dz_))

    pnts = gen_circle()
    for point in pnts:
        draw_point(window_=window, x_=c_x + point[0],
                        y_=c_y + point[1], dx_=point[2], dy_=point[3], dz_=point[4])


if __name__ == "__main__":
    master.winfo_toplevel().title("Colorful Circles")
    w.pack()

    w.bind("<Button-1>", lambda event: draw(event, w, randint(80, 245), randint(4, 35)), pi / randint(12, 120))
    master.mainloop()
