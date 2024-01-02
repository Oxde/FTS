import customtkinter as ctk
from mandelbrot import Mandelbrot
import time
from tkinter import * 
import math
import random
import pygame  #ask if we can use it?
import os #ask if we can use
from sound_generation import sound_gen
os.getcwd()


ctk.set_default_color_theme('dark-blue')

''''






'''
"0[p"
class MainWindow(ctk.CTk):
    def __init__(self,x=-0.75, y=0, m=1.5,iterations=None, imgW = None, imgH=None):
        super().__init__()
        pygame.mixer.init()
        self.setup_frames()
        self.setup_labels()
        self.setup_buttons()
        self.setup_canvas()
        ctk.set_appearance_mode('dark')
        

        self.img = None
        self.canvasW = 540
        self.canvasH = 675
        self.title('FractalToSound')
        self.geometry('800x800')
        self.fractal = Mandelbrot(self.canvasW, self.canvasH, x=x, y=y, m=m, iterations=iterations, w=imgW, h=imgH)
        self.setPalette()
        self.pixelColors = []
        self.img = None
        self.draw()
        self.entryamount = ctk.StringVar()
        self.entryamount.set(self.fractal.iterations)
        self.entry1 = ctk.CTkEntry(master=self,width=55,height=38,textvariable = self.entryamount, placeholder_text=f'{self.fractal.iterations}', font=('Impact', 25))
        self.entry1.place(x=716, y=285)

        self.setup_menu()
        
    def setup_canvas(self):
        #main_canvas is the place where iage basically is
        self.main_canvas = Canvas(master=self, height=675, width=540, background='#212121', highlightthickness=0)
        self.main_canvas.place(x=25, y=100)
        self.main_canvas.bind("<Button-1>", self.canvas_scalein)
        self.main_canvas.bind("<Button-3>", self.canvas_scaleout)
    
    def setup_menu(self):
        #setup menu obbjects to appear
        self.frame_4 = ctk.CTkFrame(master=self, width=800, height=800, fg_color= '#1A1A1A')
        self.frame_4.place(x=0, y=0)

        self.openmainwindow = ctk.CTkButton(master=self, width=340, height=60, text='Open project', font=('Impact', 25),
                                    command=self.openproject)
        self.openmainwindow.place(x=230, y=370)

    def setup_menu_light(self):
        #setup menu obbjects to appear
        self.frame_4 = ctk.CTkFrame(master=self, width=800, height=800, fg_color= '#F2F2F2')
        self.frame_4.place(x=0, y=0)

        self.openmainwindow = ctk.CTkButton(master=self, width=340, height=60, text='Open project', font=('Impact', 25), fg_color='#CD3700', hover_color='#8B2500', text_color='black',
                                    command=self.openproject)
        self.openmainwindow.place(x=230, y=370)


    def generate(self): #Это для итераций, посмотри ибо у меня не работает
         
         self.fractal.iterations = int(self.entryamount.get())
         
         self.drawPixels_image()
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
        

    def setup_buttons(self):
        # setuping buttons
        # TODO Change buttons LVLS, zoom in and zoom out. Add color adjusting, button for multi threading ( just yes or no) and restart button
        self.ldmode = ctk.CTkButton(master=self, width=170, height=30, text='Light', font=('Impact', 25),
                                    command=self.changemodelight)
        self.ldmode.place(x=600, y=730)
        self.returntomenu = ctk.CTkButton(master=self, width=170, height=30, text='Back to menu', font=('Impact', 25),
                                    command=self.hideeverything)
        self.returntomenu.place(x=600, y=685)
        self.chcolor = ctk.CTkButton(master=self, width=170, height=30, text='Random Color', font=('Impact', 25),
                                    command=self.randomPalette)
        self.chcolor.place(x=600, y=150)
        self.opencolors = ctk.CTkButton(master=self, width=170, height=30, text='Choose Colors', font=('Impact', 25),
                                    command=self.showcolors)
        self.opencolors.place(x=600, y=195)
        self.play = ctk.CTkButton(master=self, width=170, height=30, text='Play', font=('Impact', 25),
                                  command=self.play_sound)
        self.play.place(x=600, y=105)
        # color buttons
        self.red = ctk.CTkButton(master=self, width=80, height=30, text=' ', font=('Impact', 25), state = DISABLED, fg_color = self.name1._bg_color,
                                    command=self.redColor)
        self.red.place(x=600, y=240)

        self.blue = ctk.CTkButton(master=self, width=80, height=30, text=' ', font=('Impact', 25), state = DISABLED, fg_color = self.name1._bg_color,
                                    command=self.blueColor)
        self.blue.place(x=690, y=240)

        self.blue = ctk.CTkButton(master=self, width=80, height=30, text=' ', font=('Impact', 25), state = DISABLED, fg_color = self.name1._bg_color,
                                    command=self.blueColor)
        self.blue.place(x=600, y=285)

        self.green = ctk.CTkButton(master=self, width=80, height=30, text=' ', font=('Impact', 25), state = DISABLED, fg_color = self.name1._bg_color,
                                    command=self.greenColor)
        self.green.place(x=690, y=240)

        self.yellow = ctk.CTkButton(master=self, width=80, height=30, text=' ', font=('Impact', 25), state = DISABLED, fg_color = self.name1._bg_color,
                                    command=self.yellowColor)
        self.yellow.place(x=690, y=285)

        self.pink = ctk.CTkButton(master=self, width=80, height=30, text=' ', font=('Impact', 25), state = DISABLED, fg_color = self.name1._bg_color,
                                    command=self.pinkColor)
        self.pink.place(x=690, y=330)

        self.cyan = ctk.CTkButton(master=self, width=80, height=30, text=' ', font=('Impact', 25), state = DISABLED, fg_color = self.name1._bg_color,
                                    command=self.cyanColor)
        self.cyan.place(x=600, y=330)

        self.white = ctk.CTkButton(master=self, width=80, height=30, text=' ', font=('Impact', 25), state = DISABLED, fg_color = self.name1._bg_color,
                                    command=self.whiteColor)
        self.white.place(x=600, y=375)

        self.zoomreset = ctk.CTkButton(master=self, width=170, height=30, text='Reset zoom', font=('Impact', 25),
                                       command = self.resetzoom)
        self.zoomreset.place(x=600, y=240)

        self.generatation = ctk.CTkButton(master=self, width=170, height=30, text='Generate', font=('Impact', 25),
                                          command= self.generate)
        self.generatation.place(x=600, y=330)

        self.multi = ctk.CTkSwitch(master=self, width=170, height=40, switch_width= 40, switch_height=25, font=('Impact', 18), text='Multiprocessing', bg_color="#212121")
        self.multi.place(x=600, y=375)

        self.iterationslabel = ctk.CTkLabel(master=self, text='Iterations:', bg_color='#212121', text_color='#D6D6D6',
                                  font=('Impact', 25))
        self.iterationslabel.place(x=600, y=285)         

    def resetzoom(self):
        self.fractal = Mandelbrot(self.canvasW, self.canvasH,x=-1.075, y=0, m=1.5, iterations=self.fractal.iterations, w=self.canvasW, h=self.canvasH)
        self.draw()
    
    def play_sound(self):
        sound_gen()
        pygame.mixer.music.load('sound.wav')
        pygame.mixer.music.play()

    

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
    
    '''' ---------------colors------------------'''
    def setRed(self):
        palette = [(0, 0, 0)]
        redb = 2 * math.pi / (random.randint(0, 128) + 128)
        for i in range(256):
            r = clamp(int(256 * (0.5 * math.sin(redb * i + 138) + 0.5)))
            palette.append((r, 0, 0))
        self.palette = palette
    
    def redColor(self): 
        self.setRed()
        self.drawPixels_image()
    
    def setBlue(self):
        palette = [(0, 0, 0)]
        blueb = 2 * math.pi / (random.randint(0, 128) + 128)
        for i in range(256):
            b = clamp(int(256 * (0.5 * math.sin(blueb * i + 138) + 0.5)))
            palette.append((0, 0, b))
        self.palette = palette

    def blueColor(self): 
        self.setBlue()
        self.drawPixels_image()

    def setGreen(self):
        palette = [(0, 0, 0)]
        greenb = 2 * math.pi / (random.randint(0, 128) + 128)
        for i in range(256):
            g = clamp(int(256 * (0.5 * math.sin(greenb * i + 138) + 0.5)))
            palette.append((0, g, 0))
        self.palette = palette
    
    def greenColor(self): 
        self.setGreen()
        self.drawPixels_image()

    def setYellow(self):
        palette = [(0, 0, 0)]
        redb = 2 * math.pi / (random.randint(0, 128) + 128)
        greenb = 2 * math.pi / (random.randint(0, 128) + 128)
        for i in range(256):
            r = clamp(int(256 * (0.5 * math.sin(redb * i + 138) + 0.5)))
            g = clamp(int(256 * (0.5 * math.sin(greenb * i + 138) + 0.5)))
            palette.append((r, g, 0))
        self.palette = palette
    
    def yellowColor(self): 
        self.setYellow()
        self.drawPixels_image()

    def setPink(self):
        palette = [(0, 0, 0)]
        redb = 2 * math.pi / (random.randint(0, 128) + 128)
        blueb = 2 * math.pi / (random.randint(0, 128) + 128)
        for i in range(256):
            r = clamp(int(256 * (0.5 * math.sin(redb * i + 138) + 0.5)))
            b = clamp(int(256 * (0.5 * math.sin(blueb * i + 138) + 0.5)))
            palette.append((r, 0, b))
        self.palette = palette
    
    def pinkColor(self): 
        self.setPink()
        self.drawPixels_image()

    def setCyan(self):
        palette = [(0, 0, 0)]
        greenb = 2 * math.pi / (random.randint(0, 128) + 128)
        blueb = 2 * math.pi / (random.randint(0, 128) + 128)
        for i in range(256):
            g = clamp(int(256 * (0.5 * math.sin(greenb * i + 138) + 0.5)))
            b = clamp(int(256 * (0.5 * math.sin(blueb * i + 138) + 0.5)))
            palette.append((0, g, b))
        self.palette = palette
    
    def cyanColor(self): 
        self.setCyan()
        self.drawPixels_image()

    def setWhite(self):
        palette = [(0, 0, 0)]
        redb = 2 * math.pi / (random.randint(0, 128) + 128)
        greenb = 2 * math.pi / (random.randint(0, 128) + 128)
        blueb = 2 * math.pi / (random.randint(0, 128) + 128)
        for i in range(256):
            r = clamp(int(256 * (0.5 * math.sin(redb * i + 138) + 0.5)))
            g = clamp(int(256 * (0.5 * math.sin(greenb * i + 138) + 0.5)))
            b = clamp(int(256 * (0.5 * math.sin(blueb * i + 138) + 0.5)))
            palette.append((r, g, b))
        self.palette = palette
    
    def whiteColor(self): 
        self.setWhite()
        self.drawPixels_image()
    '''' ---------------------------------'''

    def changePalette(self, event):
        self.setPalette()
        self.pixelColors = []
        self.getColors()
        self.drawPixels_image()
        self.main_canvas.create_image(0, 0, image=self.background, anchor=NW)
        self.main_canvas.pack(fill=BOTH, expand=1)
    # sets and applies random colors

    def randomPalette(self): 
        self.setPalette()
        self.drawPixels_image()

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
        self.xStartCenter = self.fractal.xCenter
        self.yStartCenter = self.fractal.yCenter
        self.StartDelta = self.fractal.delta
        

    def canvas_scalein(self, event):
        self.fractal.zoomIn(event)
        self.draw()
        print(event.x,event.y)

    def canvas_scaleout(self, event):  # add keybinds
        self.fractal.zoomOut(event)
        self.draw()
        print(event.x,event.y)
    def showcolors(self): 
        self.red.configure(state = ACTIVE, fg_color = '#b22222')  
        self.blue.configure(state = ACTIVE, fg_color = '#034698')  
        self.green.configure(state = ACTIVE, fg_color = 'green')
        self.yellow.configure(state = ACTIVE, fg_color = '#FCE205')
        self.pink.configure(state = ACTIVE, fg_color = '#C154C1') 
        self.cyan.configure(state = ACTIVE, fg_color = 'cyan')
        self.white.configure(state = ACTIVE, fg_color = 'white')    
        self.opencolors.configure(command = self.hidecolors, text = 'Close Colors')
        self.zoomreset.place(y=420)
        self.entry1.place(y=465)
        self.generatation.place(y=510)
        self.iterationslabel.place(y=465)
        self.multi.place(y=555)
    # making buttons invisible and disabled


    def hidecolors(self): 
        self.red.configure(state = DISABLED, fg_color = self.name._bg_color)
        self.blue.configure(state = DISABLED, fg_color = self.name._bg_color)
        self.green.configure(state = DISABLED, fg_color = self.name._bg_color)
        self.yellow.configure(state = DISABLED, fg_color = self.name._bg_color)
        self.pink.configure(state = DISABLED, fg_color = self.name._bg_color)
        self.cyan.configure(state = DISABLED, fg_color = self.name._bg_color)
        self.white.configure(state = DISABLED, fg_color = self.name._bg_color)
        self.opencolors.configure(command = self.showcolors, text = 'Choose Colors')
        self.zoomreset.place(y=240)
        self.entry1.place(y=285)
        self.generatation.place(y=330)
        self.iterationslabel.place(y=285)
        self.multi.place(y=375)

            

    
    def changemodelight(self):
            ctk.set_appearance_mode('light')
            self.name.configure(bg_color='#E5E5E5', text_color="#CD3700")
            
            self.ldmode.configure(command=self.changemodedark, fg_color='#CD3700', text='Dark', hover_color='#8B2500',
                                  text_color='black')
            self.chcolor.configure(fg_color='#CD3700', hover_color='#8B2500', text_color='black')
            self.opencolors.configure(fg_color='#CD3700', hover_color='#8B2500', text_color='black')
            self.play.configure(fg_color='#CD3700', hover_color='#8B2500', text_color='black')
            self.zoomreset.configure(fg_color='#CD3700', hover_color='#8B2500', text_color='black')
            self.main_canvas.configure(background='#E5E5E5')
            self.returntomenu.configure(fg_color='#CD3700', hover_color='#8B2500', text_color='black')
            self.generatation.configure(fg_color='#CD3700', hover_color='#8B2500', text_color='black')
            self.name1.configure(bg_color='#E5E5E5', text_color='Black')
            self.iterationslabel.configure(text_color='black', bg_color='#E5E5E5')
            self.multi.configure(bg_color='#E5E5E5', progress_color = '#CD3700')
            if self.red._state == DISABLED:
                self.red.configure(state = DISABLED, fg_color = self.name._bg_color)
                self.blue.configure(state = DISABLED, fg_color = self.name._bg_color)
                self.green.configure(state = DISABLED, fg_color = self.name._bg_color)
                self.yellow.configure(state = DISABLED, fg_color = self.name._bg_color)
                self.pink.configure(state = DISABLED, fg_color = self.name._bg_color)
                self.cyan.configure(state = DISABLED, fg_color = self.name._bg_color)
                self.white.configure(state = DISABLED, fg_color = self.name._bg_color)


    def changemodedark(self):
        ctk.set_appearance_mode('dark')
        self.ldmode.configure(command=self.changemodelight, text='Light', fg_color='#1F538D', hover_color='#14375E',
                                 text_color='white')
        self.name.configure(bg_color='#212121', text_color='#1F538D')
        
        self.chcolor.configure(fg_color='#1F538D', hover_color='#14375E', text_color='white')
        self.opencolors.configure(fg_color='#1F538D', hover_color='#14375E', text_color='white')
        self.returntomenu.configure(fg_color='#1F538D', hover_color='#14375E', text_color='white')
        self.play.configure(fg_color='#1F538D', hover_color='#14375E', text_color='white')
        self.zoomreset.configure(fg_color='#1F538D', hover_color='#14375E', text_color='white')
        self.main_canvas.configure(background='#212121')
        self.generatation.configure(fg_color='#1F538D', hover_color='#14375E', text_color='white')
        self.iterationslabel.configure(text_color='#D6D6D6', bg_color='#212121')
        self.name1.configure(bg_color='#212121', text_color='#D6D6D6')
        self.multi.configure(bg_color='#212121', progress_color = '#1F538D')
        if self.red._state == DISABLED:
            self.red.configure(state = DISABLED, fg_color = self.name._bg_color)
            self.blue.configure(state = DISABLED, fg_color = self.name._bg_color)
            self.green.configure(state = DISABLED, fg_color = self.name._bg_color)
            self.yellow.configure(state = DISABLED, fg_color = self.name._bg_color)
            self.pink.configure(state = DISABLED, fg_color = self.name._bg_color)
            self.cyan.configure(state = DISABLED, fg_color = self.name._bg_color)
            self.white.configure(state = DISABLED, fg_color = self.name._bg_color)
    
    
    def hideeverything(self):
        if self.ldmode._command == self.changemodelight:
            self.setup_menu()
        if self.ldmode._command == self.changemodedark:
            self.setup_menu_light()

    def openproject(self):
        self.frame_4.destroy()
        self.openmainwindow.destroy()
        
         

 

def clamp(x):
    return max(0, min(x, 255))

if __name__ == '__main__':
    program = MainWindow(imgH=685, imgW=600, iterations=150)
    
    program.mainloop()
    