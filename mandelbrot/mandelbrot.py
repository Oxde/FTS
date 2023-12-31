from multiprocessing import Pool

import sys
import os


class Mandelbrot():
    def __init__(self, canvasW, canvasH, x=-0.75, y=0, m=1.5, iterations=None, w=None, h=None, zoomFactor=0.1):
        self.w, self.h = (round(canvasW*0.9), round(canvasH*0.9)) if None in {w, h} else w, h
        self.iterations = 200 if iterations is None else iterations
        self.xCenter, self.yCenter = x, y
        if canvasW > canvasH:
            self.xDelta = m/(canvasH/canvasW)
            self.yDelta = m
        else:
            self.yDelta = m/(canvasW/canvasH)
            self.xDelta = m
        self.delta = m
        self.xmin = x - self.xDelta
        self.xmax = x + self.xDelta
        self.ymin = y - self.yDelta
        self.ymax = y + self.yDelta
        self.zoomFactor = zoomFactor
        self.yScaleFactor = self.h/canvasH
        self.xScaleFactor = self.w/canvasW
        self.c, self.z = 0, 0

    def zoomOut(self, event):
        """
           Zooms out of the Mandelbrot set at the point of a mouse event.

           Adjusts the view center and scale factors based on the mouse click position.
           The view is zoomed out by a predefined zoom factor, decreasing the detail level.
           """
        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xDelta /= self.zoomFactor
        self.yDelta /= self.zoomFactor
        self.delta /= self.zoomFactor
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def zoomIn(self, event):
        """
           Zooms into the Mandelbrot set at the point of a mouse event.

           Adjusts the view center and scale factors based on the mouse click position.
           The view is zoomed in by a predefined zoom factor, increasing the detail level.
           """

        self.xCenter = translate(event.x*self.xScaleFactor, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y*self.yScaleFactor, self.h, 0, self.ymin, self.ymax)
        self.xDelta *= self.zoomFactor
        self.yDelta *= self.zoomFactor
        self.delta *= self.zoomFactor
        self.xmax = self.xCenter + self.xDelta
        self.ymax = self.yCenter + self.yDelta
        self.xmin = self.xCenter - self.xDelta
        self.ymin = self.yCenter - self.yDelta

    def getPixels(self):
        """
           Calculates the Mandelbrot set pixel data for the current view.

           Iterates over each pixel in the view, computes its corresponding complex number,
           and determines how quickly it escapes to infinity (if at all).
           Uses multiprocessing to speed up the calculation.
           TODO add option not to use multiprocessing
           """

        coordinates = []
        for x in range(self.w):
            for y in range(self.h):
                coordinates.append((x, y))
        pool = Pool()
        self.pixels = pool.starmap(self.getEscapeTime, coordinates)
        pool.close()
        pool.join()

    def getEscapeTime(self, x, y):
        """
           Determines the escape time for a given pixel in the Mandelbrot set.

           Translates pixel coordinates to complex plane coordinates and iteratively
           applies the Mandelbrot function to determine the escape time,
           i.e., the number of iterations it takes for the point to escape to infinity,
           capped by the maximum number of iterations.
           """
        re = translate(x, 0, self.w, self.xmin, self.xmax)
        im = translate(y, 0, self.h, self.ymax, self.ymin)
        z, c = complex(re, im), complex(re, im)
        for i in range(1, self.iterations):
            if abs(z) > 2:
                return (x, y, i)
            z = z*z + c
        return (x, y, 0)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)
