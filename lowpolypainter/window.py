# Python Modules
import time
import numpy as np
from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox

# Local Modules
from store import save, load
from export import exportDialog
from canvas.frame import CanvasFrame
from zoomTransformer import ZoomTransformer
from Colorwheel import Colorwheel


class Window(object):
    """
    Window Class

    Description:
    Contains canvas and roots the application.
    """

    def __init__(self, inputimage):
        self.root = Tk()

        self.zoom = ZoomTransformer()

        self.inputimage = inputimage

        # Settings
        self.root.minsize(800, 400)
        self.root.config(bg='white')
        self.root.resizable(True, False)
        self.root.title('Low Poly Painter')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        # print 'DPI value: %f' % self.root.winfo_fpixels('1i')

        # Frame
        self.frame = Frame(self.root, bg='white')
        self.frame.grid(sticky=N+S+E+W)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)

        # Toolbar Frame
        self.toolbarFrame = ToolbarFrame(self)
        self.toolbarFrame.grid(row=0, column=0, columnspan=2, sticky=N+E+W)

        self.frame.bind_all("<MouseWheel>", self.mouse_wheel_wheel)
        self.frame.bind_all("<Button-4>", self.mouse_wheel_button)
        self.frame.bind_all("<Button-5>", self.mouse_wheel_button)

        # Canvas Frame
        self.canvasFrame = CanvasFrame(self, inputimage)
        self.canvasFrame.grid(row=1, column=0, sticky=NSEW)

        # Detail Frame
        self.detailFrame = DetailFrame(self)
        self.detailFrame.grid(row=1, column=1, sticky=NSEW)

        self.colorWheel = Colorwheel(self)

    def clear(self, event=None):
        self.canvasFrame.clear()

    def export(self, event=None):
        exportDialog(self.canvasFrame.mesh, self.canvasFrame.width, self.canvasFrame.height)

    def saveMeshData(self, event=None):
        save(self.canvasFrame.mesh.save(), self.inputimage)

    def loadMeshData(self, event=None):
        self.canvasFrame.mesh.load(load(self.inputimage))

    def triangulate(self, event=None):
        self.canvasFrame.canny()

    def mouse_wheel_button(self, event):
        if event.num == 4:
            self.mouse_wheel(120, 0, 0)
        elif event.num == 5:
            self.mouse_wheel(-120, 0, 0)

    def mouse_wheel_wheel(self, event):
        self.mouse_wheel(event.delta, event.x, event.y)

    def mouse_wheel(self, delta, x, y):
        self.zoom.ZoomAt(2**(delta * 0.001), [x, y])
        self.canvasFrame.mesh.updatePositions()

    # Modechanging with Buttons
    def changeCModetoNPAL(self, event):
        self.canvasFrame.ControlMode = "NewPointAndLine"
    def changeCModetoNPO(self, event):
        self.canvasFrame.ControlMode = "NewPointOnly"
    def changeCModetoGC(self, event):
        self.canvasFrame.ControlMode = "GetColor"
    def changeCModetoUC(self, event):
        self.canvasFrame.ControlMode = "UseColor"
    def changeCModetoCU(self, event):
        self.canvasFrame.ControlMode = "ColorUnlock"

class ToolbarFrame(Frame):
    """
    Toolbar Frame Class

    Description:
    Contains tools and visual states of canvas
    """
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent.frame)
        self.parent = parent
        self.config(bg='#DADADA', width=47)
        self.grid_columnconfigure(0, weight=1)

        self.buttonFrame = ButtonFrame(self)
        self.buttonFrame.grid(row=0, sticky=N+E+S+W)

        self.bottomBorder = Frame(self, bg='#AAAAAA', height=1)
        self.bottomBorder.grid(row=1, sticky=N+E+S+W)

class ButtonFrame(Frame):
    """
    Button Frame Class

    Description:
    Contains two buttons for clearing and testing.
    """
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent)
        self.config(bg='#DADADA', height=46)
        self.grid_columnconfigure(4, weight=1)
        # self.grid_rowconfigure(0, weight=0)

        icon_0 = PhotoImage(file="./lowpolypainter/resources/icons/Insert.gif")
        icon_1 = PhotoImage(file="./lowpolypainter/resources/icons/Clear.gif")
        icon_2 = PhotoImage(file="./lowpolypainter/resources/icons/Canny.gif")
        icon_3 = PhotoImage(file="./lowpolypainter/resources/icons/Color.gif")
        icon_4 = PhotoImage(file="./lowpolypainter/resources/icons/Save.gif")
        icon_5 = PhotoImage(file="./lowpolypainter/resources/icons/Export.gif")
        icon_6 = PhotoImage(file="./lowpolypainter/resources/icons/PandL.gif")
        icon_7 = PhotoImage(file="./lowpolypainter/resources/icons/P.gif")
        icon_8 = PhotoImage(file="./lowpolypainter/resources/icons/GetColor.gif")
        icon_9 = PhotoImage(file="./lowpolypainter/resources/icons/UseColor.gif")
        icon_10 = PhotoImage(file="./lowpolypainter/resources/icons/ColorUnlock.gif")

        options = {"height": 46, "width": 46, "bg":'#DADADA', "borderwidth":0}

        # Insert Button
        self.insertButton = Label(self, image=icon_0, **options)
        self.insertButton.image = icon_0
        self.insertButton.grid(row=0, column=0, sticky=N+E+S+W)
        # self.insertButton.bind("<Button-1>", parent.parent.clear)

        # Clear Button
        self.clearButton = Label(self, image=icon_1, **options)
        self.clearButton.image = icon_1
        self.clearButton.grid(row=0, column=1, sticky=N+E+S+W)
        self.clearButton.bind("<Button-1>", parent.parent.clear)

        # Canny Button
        self.cannyButton = Label(self, image=icon_2, **options)
        self.cannyButton.image = icon_2
        self.cannyButton.grid(row=0, column=2, sticky=N+E+S+W)
        self.cannyButton.bind("<Button-1>", parent.parent.triangulate)


        # Modechaning Buttons

        # NewPointAndLine Button
        self.modeOneButton = Label(self, image=icon_6, **options)
        self.modeOneButton.image = icon_6
        self.modeOneButton.grid(row=0, column=3, sticky=N+E+S+W)
        self.modeOneButton.bind("<Button-1>", parent.parent.changeCModetoNPAL)
        # NewPointOnly Button
        self.modeTwoButton = Label(self, image=icon_7, **options)
        self.modeTwoButton.image = icon_7
        self.modeTwoButton.grid(row=0, column=4, sticky=N + E + S + W)
        self.modeTwoButton.bind("<Button-1>", parent.parent.changeCModetoNPO)
        # GetColor Button
        self.modeThreeButton = Label(self, image=icon_8, **options)
        self.modeThreeButton.image = icon_8
        self.modeThreeButton.grid(row=0, column=5, sticky=N + E + S + W)
        self.modeThreeButton.bind("<Button-1>", parent.parent.changeCModetoGC)
        # Use Color Button
        self.modeFourButton = Label(self, image=icon_9, **options)
        self.modeFourButton.image = icon_9
        self.modeFourButton.grid(row=0, column=6, sticky=N + E + S + W)
        self.modeFourButton.bind("<Button-1>", parent.parent.changeCModetoUC)
        # Color Unlock
        self.modeFiveButton = Label(self, image=icon_10, **options)
        self.modeFiveButton.image = icon_10
        self.modeFiveButton.grid(row=0, column=7, sticky=N + E + S + W)
        self.modeFiveButton.bind("<Button-1>", parent.parent.changeCModetoCU)





        # Space
        self.space = Label(self, height=2, bg='#DADADA', borderwidth=0)
        self.space.grid(row=0, column=8, sticky=N+E+S+W)

        # Save Button
        self.saveButton = Label(self, image=icon_4, **options)
        self.saveButton.image = icon_4
        self.saveButton.grid(row=0, column=9, sticky=N+E+S+W)
        self.saveButton.bind("<Button-1>", parent.parent.saveMeshData)

        # Export Button
        self.exportButton = Label(self, image=icon_5, **options)
        self.exportButton.image = icon_5
        self.exportButton.grid(row=0, column=10, sticky=N+E+S+W)
        self.exportButton.bind("<Button-1>", parent.parent.export)

class DetailFrame(Frame):
    """
    Detail Frame Class

    Description:
    Contains details about current selected tool
    """
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent.frame)
        self.config(bg='#ECECEC', width=200)

        self.grid_rowconfigure(0, weight=1)

        self.informationFrame = Frame(self, bg='#ECECEC', width=199)
        self.informationFrame.grid(row=0, column=1, sticky=N+E+S+W)

        self.leftBorder = Frame(self, bg='#AAAAAA', width=1)
        self.leftBorder.grid(row=0, column=0, sticky=N+E+S+W)

# TODO: Move description to tags
"""
Place, select and move points and lines with the mouse.
A line to the next point will automatically be created, as long as CTRL is not pressed.
Faces are selected by simply clicking on them.
Please note that there is no visualisation if you select any face.
To connect two points with a line, or to split a line in two, hold the SHIFT button.
If a line creates one or more triangles, then they will be automatically added.
Delete selected objects with DEL.
Toggle the visibility of the faces with SPACE.
"""
