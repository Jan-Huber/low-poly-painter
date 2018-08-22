# Python Modules
import time
import numpy as np
from Tkinter import *
from PIL import ImageTk, Image

# Local Modules
from mesh import Mesh
from lowpolypainter.canny import Canny
from lowpolypainter.color import Color

class CanvasFrame(Frame):
    """
    Canvas Frame Class

    Description:
    Contains the loaded image and sets the mouse button click event
    """

    def __init__(self, parent, inputimage, *args, **kwargs):
        Frame.__init__(self, parent.frame)

        # Parent
        self.parent = parent

        # Load Image
        self.inputimage = inputimage
        filepath = 'lowpolypainter/resources/images/' + inputimage
        self.image = Image.open(filepath)
        self.background = ImageTk.PhotoImage(self.image)

        # Center Canvas 
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Create Canvas
        self.width = self.background.width()
        self.height = self.background.height()
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.create_image(1, 1, image=self.background, anchor=NW)
        self.canvas.grid(row=1, column=1, sticky=NSEW)

        # Color Object
        self.color = Color(np.array(self.image), 0.5, 0.5)

        self.selectedFace = [False, None]

        # Mesh
        self.mesh = Mesh(self)

        # Selection
        self.selected = None

         # Mouse Event
        self.mouseEvent = False
        self.faceState = NORMAL

        # Controls
        self.ControlMode = "NewPointAndLine"

        # Reading settings
        with open("./lowpolypainter/resources/settings.config", 'r') as settings:
            l = settings.readlines()

        # Events
        self.canvas.bind("<Button>", self.click)
        self.canvas.bind_all("<space>", func=self.toggleFaces)
        self.canvas.bind_all(l[0][0], self.changeCModetoNPAL)
        self.canvas.bind_all(l[1][0], self.changeCModetoNPO)
        self.canvas.bind_all(l[2][0], self.changeCModetoUC)
        self.canvas.bind_all("<BackSpace>", self.deleteSelected)
        self.canvas.bind_all("<Key-Delete>", self.deleteSelected)
        self.canvas.bind_all(l[3][0], self.changeCModetoGC)
        self.canvas.bind_all(l[4][0], self.changeCModetoCU)

    """ EVENT """
    def click(self, event):
        """
        Canvas Click Event

        Description:
        Adds point to canvas, will draw line to last point while ctrl isn't pressed
        """

        """
        eventPoint = [event.x, event.y]
        if self.inBounds(eventPoint) and not self.mouseEvent:
            previousSelected = self.selected
            zoomedCoords = self.parent.zoom.FromViewport([event.x, event.y])
            self.mesh.addVertex([int(zoomedCoords[0]), int(zoomedCoords[1])])
            if (previousSelected is not None) and not (event.state & CTRL_MASK):
                self.mesh.addEdge(previousSelected, self.selected)
        self.mouseEventHandled = False
        
        """
        if self.mouseEvent:
            return
        elif (self.ControlMode=="NewPointAndLine"):
            eventPoint = [event.x, event.y]
            if self.inBounds(eventPoint):
                previousSelected = self.selected
                zoomedCoords = self.parent.zoom.FromViewport([event.x, event.y])
                self.mesh.addVertex([int(zoomedCoords[0]), int(zoomedCoords[1])])
                if (previousSelected is not None):
                    self.mesh.addEdge(previousSelected, self.selected)
        elif (self.ControlMode=="NewPointOnly"):
            eventPoint = [event.x, event.y]
            if self.inBounds(eventPoint):
                previousSelected = self.selected
                zoomedCoords = self.parent.zoom.FromViewport([event.x, event.y])
                self.mesh.addVertex([int(zoomedCoords[0]), int(zoomedCoords[1])])



    """ FACE """
    def toggleFaces(self, event):
        state = NORMAL
        if self.faceState is NORMAL:
            state = HIDDEN
        self.canvas.itemconfigure("f", state=state)
        self.faceState = state

    """ GENERAL """
    def inBounds(self, point):
        x, y = point[0], point[1]
        return (x >= 0) and (y >= 0) and (x < self.width) and (y < self.height)

    def select(self, object):
        if (object != self.selected):
            self.deselect(self.selected)
            self.selected = object

    def deleteSelected(self, event):
        if self.selected is not None:
            self.selected.delete()
            self.selected = None

    def deselect(self, object):
        if self.selected is not None:
            object.deselect()

    def clear(self):
        self.selectedFace = [False, None]
        self.mesh.clear()

    # Modechanging with Keys
    def changeCModetoNPAL(self, event):
        self.ControlMode = "NewPointAndLine"

    def changeCModetoNPO(self, event):
        self.ControlMode = "NewPointOnly"

    def changeCModetoUC(self, event):
        self.ControlMode = "UseColor"

    def changeCModetoGC(self, event):
        self.ControlMode = "GetColor"

    def changeCModetoCU(self, event):
        self.ControlMode = "ColorUnlock"


    """ CANNY """
    def canny(self):
        start0 = time.clock()
        canny = Canny(self.inputimage)
        canny.generateCorners()
        canny.generateCanny(99, 100)
        triangle = canny.generateDelaunay()
        end0 = time.clock()

        start1 = time.clock()
        for tris in triangle:
            self.mesh.faceToVertexGeneration(canny.points[tris[0]],
                                             canny.points[tris[1]],
                                             canny.points[tris[2]])
        end1 = time.clock()

        start2 = time.clock()
        for face in self.mesh.faces:
            face.draw(False)
        end2 = time.clock()

        start3 = time.clock()
        for edge in self.mesh.edges:
            edge.draw(False)
        end3 = time.clock()

        start4 = time.clock()
        for vert in self.mesh.vertices:
            vert.draw()
        end4 = time.clock()

        print 'Delaunay', end0 - start0
        print 'Mesh Generation', end1 - start1
        print 'Draw Face', end2 - start2
        print 'Draw Edge', end3 - start3
        print 'Draw Vert', end4 - start4
