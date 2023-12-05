import customtkinter as ctk
from mandelbrot import Mandelbrot
import time
from tkinter import *
import math
import random

from PIL import Image, ImageTk
ctk.set_default_color_theme('dark-blue')


''''






'''
"0[p"
class MainWindow(ctk.CTk):
    def __init__(self,x=-0.75, y=0, m=1.5,iterations=None, imgW = None, imgH=None):
        super().__init__()

        self.setup_frames()
        self.setup_labels()
        self.setup_buttons()
        self.setup_canvas()
        ctk.set_appearance_mode('dark')

        self.img = None
        self.canvasW = 600
        self.canvasH = 600
        self.title('FractalToSound')
        self.geometry('800x800')
        self.fractal = Mandelbrot(self.canvasW, self.canvasH, x=x, y=y, m=m, iterations=iterations, w=imgW, h=imgH)
        self.setPalette()
        self.pixelColors = []
        self.img = None
        self.draw()


    def setup_frames(self):
        # setuping frames
        self.frame_1 = ctk.CTkFrame(master=self, width=760, height=55)
        self.frame_1.place(x=20, y=20)
        self.frame_2 = ctk.CTkFrame(master=self, width=550, height=685)
        self.frame_2.place(x=20, y=95)
        self.frame_3 = ctk.CTkFrame(master=self, width=190, height=685)
        self.frame_3.place(x=590, y=95)

    def setup_labels(self):
        # setuping labels
        self.name = ctk.CTkLabel(master=self, text='FractalToSound', bg_color='#212121', text_color='#1F538D',
                                 font=('Impact', 35))
        self.name.place(x=300, y=25)
        self.name1 = ctk.CTkLabel(master=self, text='To', bg_color='#212121', text_color='white',
                                  font=('Impact', 35))
        self.name1.place(x=400, y=25)
        self.levels = ctk.CTkLabel(master=self, text='Levels:', bg_color='#212121', font=('Impact', 30))
        self.levels.place(x=605, y=105)

    def setup_buttons(self):
        # setuping buttons
        # TODO Change buttons LVLS, zoom in and zoom out. Add color adjusting, button for multi threading ( just yes or no) and restart button
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
        #main_canvas is the place where iage basically is
        self.main_canvas = Canvas(master=self, height=675, width=540, background='#212121', highlightthickness=0)
        self.main_canvas.place(x=25, y=100)
        self.main_canvas.bind("<Button-1>", self.canvas_scalein)
        self.main_canvas.bind("<Button-3>", self.canvas_scaleout)

    '''' ---------------methods------------------'''
    def setPalette(self):
        # sets pallete ( basically colors) to a random values, so fractal looks nice when zooming
        # probably nice idea to add second mode, where colors can be manually chosed

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
        self.drawPixels_image()
        self.main_canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.main_canvas.pack(fill=BOTH, expand=1)

    def getColors(self):
        pixelColors = []
        for p in self.fractal.pixels:
            pixelColors.append(self.palette[p[2] % 256])
        self.pixelColors = pixelColors



    def drawPixels_image(self):
        """
                Generates and displays the Mandelbrot set as an image on the canvas.

                This method creates a PPM (Portable Pixmap) format image string from the calculated
                Mandelbrot set pixels. The PPM image is then loaded into a PhotoImage object and
                displayed on the canvas widget.

                The PPM format starts with a header indicating the image format, dimensions, and
                maximum color value. The image data consists of RGB color values for each pixel.
                """
        ppm_header = f'P6 {self.fractal.w} {self.fractal.h} 255\n'

        # Initialize an empty image data array
        ppm_data = bytearray([0, 0, 0] * self.fractal.w * self.fractal.h)

        # Set the pixels
        for p in self.fractal.pixels:
            index = int(p[1]) * self.fractal.w + int(p[0])  # Calculate the index for linear array
            color = self.palette[p[2] % 256]
            ppm_data[index * 3:index * 3 + 3] = color

        # Combine header and data to form PPM image string
        ppm_image = ppm_header.encode() + ppm_data
        # Load PPM image string into PhotoImage
        self.background = PhotoImage(data=ppm_image)
        # Display the image on the canvas
        self.main_canvas.create_image(0, 0, image=self.background, anchor=NW)

    def draw(self):
        """
               Main method to initiate the drawing of the Mandelbrot set.

               This method triggers the calculation of the Mandelbrot set, maps the iteration
               counts to colors, and then calls drawPixels_image to render the image. It also
               prints the time taken to process the drawing and the current coordinates of the
               fractal view.
               """
        print('-' * 20)
        start = time.time()
        self.fractal.getPixels()
        self.getColors()
        self.drawPixels_image()  # Use the new method for drawing
        print("Process took {} seconds".format(round(time.time() - start, 2)))
        print("Current coordinates (x, y, m): {}, {}, {}".format(self.fractal.xCenter, self.fractal.yCenter,
                                                                 self.fractal.delta))

    def canvas_scalein(self, event):
        self.fractal.zoomIn(event)
        self.draw()
        print(event.x,event.y)

    def canvas_scaleout(self, event):  # add keybinds
        self.fractal.zoomOut(event)
        self.draw()
        print(event.x,event.y)

    def changemodelight(self):
            ctk.set_appearance_mode('light')
            self.name.configure(bg_color='#E5E5E5', text_color="#CD3700")
            self.levels.configure(bg_color='#E5E5E5')
            self.ldmode.configure(command=self.changemodedark, fg_color='#CD3700', text='Dark', hover_color='#8B2500',
                                  text_color='black')
            self.generate.configure(fg_color='#CD3700', hover_color='#8B2500', text_color='black')
            self.play.configure(fg_color='#CD3700', hover_color='#8B2500', text_color='black')
            self.main_canvas.configure(background='#E5E5E5')
            self.zoomin.configure(fg_color='#CD3700', hover_color='#8B2500', text_color='black')
            self.zoomout.configure(fg_color='#CD3700', hover_color='#8B2500', text_color='black')
            self.name1.configure(bg_color='#E5E5E5', text_color='Black')

    def changemodedark(self):
        ctk.set_appearance_mode('dark')
        self.ldmode.configure(command=self.changemodelight, text='Light', fg_color='#1F538D', hover_color='#14375E',
                                 text_color='white')
        self.name.configure(bg_color='#212121', text_color='#1F538D')
        self.levels.configure(bg_color='#212121')
        self.generate.configure(fg_color='#1F538D', hover_color='#14375E', text_color='white')
        self.play.configure(fg_color='#1F538D', hover_color='#14375E', text_color='white')
        self.main_canvas.configure(background='#212121')
        self.zoomin.configure(fg_color='#1F538D', hover_color='#14375E', text_color='white')
        self.zoomout.configure(fg_color='#1F538D', hover_color='#14375E', text_color='white')
        self.name1.configure(bg_color='#212121', text_color='white')


def clamp(x):
    return max(0, min(x, 255))

if __name__ == '__main__':
    program = MainWindow(imgH=600, imgW=600,iterations=150)
    program.mainloop()
