import customtkinter as ctk
from mandelbrot import Mandelbrot
import time
from tkinter import *
import math
import random

from PIL import Image, ImageTk
ctk.set_default_color_theme('dark-blue')



class MainWindow(ctk.CTk):
    def init(self,x=-0.3,y=0,m=1.5,iterations=None, imgW = None, imgH=None):
        super().init()

        self.setup_frames()
        self.setup_labels()
        self.setup_buttons()
        self.setup_canvas()
        ctk.set_appearance_mode('dark')

        self.img = None
        self.canvasW = 700
        self.canvasH = 600
        self.title('FractalToSound')
        self.geometry('800x800')
        self.fractal = Mandelbrot(self.canvasW, self.canvasH, x=x, y=y, m=m, iterations=iterations, w=imgW, h=imgH)
        self.setPalette()
        self.pixelColors = []
        self.img = None
        self.draw()

        self.bind("<Button-1>", self.canvas_scalein)
        self.bind("<Button-3>", self.canvas_scaleout)

    def setup_frames(self):
        self.frame_1 = ctk.CTkFrame(master=self, width=760, height=55)
        self.frame_1.place(x=20, y=20)
        self.frame_2 = ctk.CTkFrame(master=self, width=550, height=685)
        self.frame_2.place(x=20, y=95)
        self.frame_3 = ctk.CTkFrame(master=self, width=190, height=685)
        self.frame_3.place(x=590, y=95)

    def setup_labels(self):
        self.name = ctk.CTkLabel(master=self, text='FractalToSound', bg_color='#212121', text_color='#1F538D',
                                 font=('Impact', 35))
        self.name.place(x=300, y=25)
        self.name1 = ctk.CTkLabel(master=self, text='To', bg_color='#212121', text_color='white',
                                  font=('Impact', 35))
        self.name1.place(x=400, y=25)
        self.levels = ctk.CTkLabel(master=self, text='Levels:', bg_color='#212121', font=('Impact', 30))
        self.levels.place(x=605, y=105)

    def setup_buttons(self):
        self.ldmode = ctk.CTkButton(master=self, width=160, height=30, text='Light', font=('Impact', 25),
                                    command=self.changemodelight)
        self.ldmode.place(x=605, y=730)
        self.generate = ctk.CTkButton(master=self, width=160, height=30, text='Generate', font=('Impact', 25))
        self.generate.place(x=605, y=150)
        self.play = ctk.CTkButton(master=self, width=160, height=30, text='Play', font=('Impact', 25))
        self.play.place(x=605, y=200)
        self.zoomin = ctk.CTkButton(master=self, width=160, height=30, text='Zoom in', font=('Impact', 25),
                                    command=self.canvas_scalein)
        self.zoomin.place(x=605, y=250)
        self.zoomout = ctk.CTkButton(master=self, width=160, height=30, text='Zoom out', font=('Impact', 25),
                                     command=self.canvas_scaleout)
        self.zoomout.place(x=605, y=300)

    def setup_canvas(self):
        self.main_canvas = Canvas(master=self, height=675, width=540, background='#212121', highlightthickness=0)
        self.main_canvas.place(x=25, y=100)

    '''' ---------------methods------------------'''
    def setPalette(self):
        palette = [(0, 0, 0)]
        redb = 2 * math.pi / (random.randint(0, 128) + 128)
        redc = 256 * random.random()
        greenb = 2 * math.pi / (random.randint(0, 128) + 128)
        greenc = 256 * random.random()
        blueb = 2 * math.pi / (random.randint(0, 128) + 128)
        bluec = 256 * random.random()
        for i in range(256):
            r = clamp(int(256 * (0.5 * math.sin(redb * i + redc) + 0.5)))
            g = clamp(int(256 * (0.5 * math.sin(greenb * i + greenc) + 0.5)))
            b = clamp(int(256 * (0.5 * math.sin(blueb * i + bluec) + 0.5)))
            palette.append((r, g, b))
        self.palette = palette

    def changePalette(self, event):
        self.setPalette()
        self.pixelColors = []
        self.getColors()
        self.drawPixels()
        self.main_canvas.create_image(0, 0, image=self.background, anchor=NW)