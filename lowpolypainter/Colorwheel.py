from Tkinter import *
from tkColorChooser import askcolor

class Colorwheel(Frame):

    # Buttonfunctions
    def firstColorUse(self):
        self.activecol = self.firstColor
        self.redraw()

    def secondColorUse(self):
        self.activecol = self.secondColor
        self.redraw()

    def thirdColorUse(self):
        self.activecol = self.thirdColor
        self.redraw()

    def firstColorSafe(self):
        self.firstColor = self.activecol
        self.firstColorButtonSafe.configure(bg=self.firstColor)
        self.firstColorButtonUse.configure(bg=self.firstColor)

    def secondColorSafe(self):
        self.secondColor = self.activecol
        self.secondColorButtonSafe.configure(bg=self.secondColor)
        self.secondColorButtonUse.configure(bg=self.secondColor)

    def thirdColorSafe(self):
        self.thirdColor = self.activecol
        self.thirdColorButtonSafe.configure(bg=self.thirdColor)
        self.thirdColorButtonUse.configure(bg=self.thirdColor)


    # Menuebuttons
    def refine(self):
        self.activecol = askcolor(self.activecol)[1]
        self.redraw()

    # Redrawing Color at the top
    def redraw(self):
        self.canvas.create_rectangle(0, 0, self.activeColorCanvasWidth+1, self.activeColorCanvasHeight+1, fill=self.activecol)

    def createWidgets(self):
        self.activeColorCanvasWidth = 50
        self.activeColorCanvasHeight = 50
        self.canvas = Canvas(self.topFrame, width=self.activeColorCanvasWidth, height=self.activeColorCanvasHeight)
        self.redraw()
        self.canvas.grid(column=0)


        self.firstColorFrame = Frame(self.bottomFrame)
        self.firstColorFrame.grid(row=0, column=0)
        self.firstColorButtonSafe = Button(self.firstColorFrame, text="Safe", fg="white", bg=self.firstColor, width=8, height=2, command=self.firstColorSafe)
        self.firstColorButtonSafe.grid()
        self.firstColorButtonUse = Button(self.firstColorFrame, text="Use", fg="white", bg=self.firstColor, width=8, height=2, command=self.firstColorUse)
        self.firstColorButtonUse.grid()


        self.secondColorFrame = Frame(self.bottomFrame)
        self.secondColorFrame.grid(row=0, column=1)
        self.secondColorButtonSafe = Button(self.secondColorFrame, text="Safe", fg="white", bg=self.secondColor, width=8, height=2, command=self.secondColorSafe)
        self.secondColorButtonSafe.grid()
        self.secondColorButtonUse = Button(self.secondColorFrame, text="Use", fg="white", bg=self.secondColor, width=8, height=2, command=self.secondColorUse)
        self.secondColorButtonUse.grid()


        self.thirdColorFrame = Frame(self.bottomFrame)
        self.thirdColorFrame.grid(row=0, column=2)
        self.thirdColorButtonSafe = Button(self.thirdColorFrame, text="Safe", fg="white", bg=self.thirdColor, width=8, height=2, command=self.thirdColorSafe)
        self.thirdColorButtonSafe.grid()
        self.thirdColorButtonUse = Button(self.thirdColorFrame, text="Use", fg="white", bg=self.thirdColor, width=8, height=2, command=self.thirdColorUse)
        self.thirdColorButtonUse.grid()

        self.menueFrame = Frame(self.bottomFrame)
        self.menueFrame.grid(row=0, column=3)
        self.REFINE = Button(self.menueFrame, text="Edit", command=self.refine)
        self.REFINE.grid()


    def __init__(self, window):
        self.window = window
        self.mesh = window.canvasFrame.mesh
        self.activecol = "grey"
        self.firstColor = "black"
        self.secondColor = "black"
        self.thirdColor = "black"

        self.mainFrame = Frame(self.window.detailFrame)
        self.mainFrame.grid(row=0)

        self.topFrame = Frame(self.mainFrame)
        self.topFrame.grid(row=0)
        self.bottomFrame = Frame(self.mainFrame)
        self.bottomFrame.grid(row=1)

        self.createWidgets()
