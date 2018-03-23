import tkinter as tk
from math import sin, cos
from random import randint

pi = 3.1415926535897932384626433832795028841971693993751058209749445923

width = 800
height = 600

r = 2
c_x = randint(100, width - 100)
c_y = randint(100, height - 100)

inc = pi / 120

dt = 100
r_max = c_x ** 2 + c_y ** 2
r_inc = 4

master = tk.Tk()
w = tk.Canvas(master, width=width, height=height)

def map_(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def draw():
    global r
    global w
    if r ** 2 > (c_x ** 2 + c_y ** 2):
        return

    i = -pi
    while i < pi:
        
        x = r * cos(i)
        y = r * sin(i)
        outline = "#{}{}{}"

        dx = int(map_(i, -pi, pi, 0, 255))
        if dx < 0:
            dx *= -1
        dy = int(map_(sin(map_(r, 0, r_max, 0, 255)), -1, 1, 0, 255))
        dz = int(map_(cos(r), -1, 1, 0, 255))

        try:
            w.create_rectangle((x + c_x, y + c_y, x + c_x, y + c_y), outline=outline.format("%02x" % dx, "%02x" % dy, "%02x" % dz))
        except Exception:
            print(dx, dy, dz)
            exit()

        i += inc

    r += r_inc
    w.after(dt, draw)

if __name__ == "__main__":
    w.pack()

    w.after(100, draw)
    master.mainloop()
