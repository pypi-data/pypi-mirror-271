import json
import tkinter
from tkinter import ttk

from magictk import color_tmpl
from magictk import photoload
from magictk import fontconfig


class Icon:
    color = color_tmpl.default_color
    size = 12
    iconname = "apple"
    setcolor = "primary"

    def _draw(self, x, y, **kwargs):
        border_info = json.loads(photoload.loadres(
            f"icon/{self.iconname}@{self.size}"))
        y_n = 0
        for i in border_info:
            x_n = 0
            for j in i:
                px = x+x_n+1
                py = y+y_n+1
                if (j < 0):
                    lcolor = -j
                else:
                    lcolor = j
                if (self.setcolor[0] == '#'):
                    g_color = color_tmpl.mix_color(
                        self.setcolor, self.color["background"], int((1-lcolor/255)*1000)/1000)
                else:
                    g_color = color_tmpl.mix_color(
                        self.color[self.setcolor], self.color["background"], int((1-lcolor/255)*1000)/1000)

                obj = self.canvas.create_rectangle(
                    py, px, py, px, width=0, fill=g_color)
                x_n += 1
            y_n += 1

    def __init__(self, master=None, size=16, iconname="apple", setcolor="regular_text", color_list: dict = None, _set_defaultcolor=None):
        self.size = size
        self.iconname = iconname
        self.setcolor = setcolor
        self.canvas = tkinter.Canvas(
            master, bg=self.color["background"], width=size+2, height=size+2, borderwidth=0, bd=0, highlightcolor=self.color["background"], highlightthickness=0)

        self._draw(0, 0)

    def pack(self, *args, **kwargs):
        self.canvas.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.canvas.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.canvas.place(*args, **kwargs)
