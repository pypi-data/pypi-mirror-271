from tkinter import Canvas, Frame, BOTH, YES
import tkinter as tk

import ctypes
from ctypes import windll
user32 = ctypes.windll.user32

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def totuple(self): return (self.x, self.y)

class Col3:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    def to_hex(self):
        return "#{:02x}{:02x}{:02x}".format(self.r,self.g,self.b)
    def to_tuple(self):
        return (self.r, self.g, self.b)

class DrawingOverlay(tk.Tk):
    def __init__(self):
        super().__init__()

        self.initWin()

    def initWin(self):
        self.attributes('-alpha', 1)
        self.attributes('-topmost', True)
        self.overrideredirect(True)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        self.center_screen = Vec2(user32.GetSystemMetrics(0) / 2, user32.GetSystemMetrics(1) / 2)
        
        window_size = 300
        x_position = (self.screen_width - window_size) // 2
        y_position = (self.screen_height - window_size) // 2
        self.geometry(f'{self.screen_width}x{self.screen_height}+0+0')
        self.wm_attributes('-transparentcolor', 'white')

        self.canvas = Canvas(self, bg='white', highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)

    def clear(self):
        self.canvas.delete("all")
    
    def draw_circle(self, rad, vec1, outline='red', width=1):
        center_x = vec1.x - rad/2
        center_y = vec1.y - rad/2
        shape = self.canvas.create_oval(center_x, center_y, center_x + rad, center_y + rad, outline=outline, width=width)

    def draw_line(self, vec1, vec2, outline='red', width=1):
        self.canvas.create_line(vec1.x, vec1.y, vec2.x, vec2.y, fill=outline, width=width)
        
    def draw_rect(self, pos, pos2, outline='red', width=1):
        self.canvas.create_rectangle(pos.x, pos.y, pos2.x, pos2.y, outline=outline, width=width) 

    def draw_rect_filled(self, pos, pos2, fill, outline='red'):
        self.canvas.create_rectangle(pos.x, pos.y, pos2.x, pos2.y, fill=fill, outline=outline) 
        
    def draw_triangle(self, vec1, vec2, vec3, outline='green', width=1):
        self.canvas.create_line(vec1.x, vec1.y, vec2.x, vec2.y, fill=outline, width=width)
        self.canvas.create_line(vec2.x, vec2.y, vec3.x, vec3.y, fill=outline, width=width)
        self.canvas.create_line(vec3.x, vec3.y, vec1.x, vec1.y, fill=outline, width=width)

    def draw_filled_triangle(self, vec1, vec2, vec3, fill='yellow', outline='red'):
        self.canvas.create_polygon(vec1.x, vec1.y, vec2.x, vec2.y, vec3.x, vec3.y, fill=fill, outline=outline)
        
    def draw_text(self, position, text, font=('Arial', 12), fill='black'):
        self.canvas.create_text(300, 50, text="HELLO WORLD", fill="black", font=('Helvetica 15 bold'))

    
def cross(color):
    col = color
    d = DrawingOverlay()
    d.draw_line(Vec2(d.screen_width/2,d.screen_height/2+10), Vec2(d.screen_width/2,d.screen_height/2-10), outline=col, width=2)
    d.draw_line(Vec2(d.screen_width/2+10,d.screen_height/2), Vec2(d.screen_width/2-10,d.screen_height/2), outline=col, width=2)
    d.mainloop()