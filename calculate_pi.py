# Module will approximate the value of PI

import tkinter as tk
from random import randint
from time import sleep
from math import sqrt

out = "Current Appx of Pi: {:0.10f}"

tdelta = 1

c_x = 800
c_y = 500

width = 2400
height = 2400
w_min = 800
h_min = 800
side = height - w_min
r = (side - w_min) * 0.5

x = c_x - r
y = c_y - r

count = 0
i_count = 1

master = tk.Tk()
w = tk.Canvas(master, width=width, height=height)

v = tk.StringVar()
tk.Label(master, textvariable=v).pack()

v.set(out.format(0))


def add_point():
    global count
    global i_count
    global master
    global w
    global w_min
    global h_min
    global side
    global l
    global v
    global r
    global x
    global y
    for i in range(1000):
    ##    x = randint(c_x - r, c_x + r)
    ##    y = randint(c_y - r, c_y + r)
        x = (x + 1) if x <= (c_x) else (c_x - r)
        if x == (c_x):
            y += 1
        else:
            if y == (c_y):
                return
        w.create_oval((x, y, x, y), fill="green", outline="green")
        count += 1
        dist = sqrt((x - c_x) ** 2 + (y - c_y) ** 2)
        if dist < r:
            i_count  += 1
        v.set(out.format(4 * i_count / count))
    master.after(tdelta, add_point)


if __name__ == "__main__":
    w.pack()

    w.create_rectangle((c_x - r, c_y - r, c_x + r, c_y + r))
    w.create_oval((c_x - r, c_y - r, c_x + r, c_y + r), tags=("circle", ))

    master.after(1000, add_point)
    master.mainloop()
