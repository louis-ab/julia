from PIL import Image as image, ImageTk
import tkinter as tk
import ctypes
import numpy as np
from time import sleep
import argparse
from random import random

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--position", help="julia set position")
arg = parser.parse_args().position

# parse argument
if arg is not None:
    if '+' in arg:
        cx = float(arg.split('+')[0])
        cy = float(arg.split('+')[1][:-1])
    elif '-' in arg[1:]:
        if arg[0] == '-':
            cx = -float(arg.split('-')[1])
        else:
            cx = float(arg.split('-')[0])
        cy = -float(arg[1:].split('-')[-1][:-1])
    elif 'i' in arg:
        cx = 0
        cy = float(arg[:-1])
    else:
        cx = float(arg)
else:
    cx = random()*2-1
    cy = random()*2-1

prec = 300
zoomstep = 2
w,h = 1000, 1000
x,y,z = 0,0,2.5

im = np.zeros((h,w,3),dtype=np.int32)

# initialize C types
fc = ctypes.CDLL("./julia.o")
fc.julia.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
fc.julia.restype = None
imc = im.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

# initialize tkinter
root = tk.Tk()
root.geometry(str(w+2)+'x'+str(h+2))
canvas = tk.Canvas(root,width=w,height=h)
canvas.pack()

def zoom(event,o):
    global x,y,z
    x += z*event.x/w-z/2
    y -= z*event.y/h-z/2
    if o:
        z *= zoomstep
    else:
        z /= zoomstep
    render()

def render():
    global imt
    fc.julia(cx,cy,x-z/2,x+z/2,y-z/2,y+z/2,w,prec,imc)
    imt = ImageTk.PhotoImage(image.fromarray(im.astype(np.uint8)))
    canvas.create_image(w//2+1,h//2+1,image=imt)

root.bind("<Button-1>", lambda event: zoom(event,0))
root.bind("<Button-3>", lambda event: zoom(event,1))

render()
root.mainloop()
