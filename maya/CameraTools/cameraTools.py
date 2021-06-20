""" Camera Tools
    Description:
                = Tool for creating and controlling the attributes of multiple cameras and their imagePlanes. Can be exapnded to include more attributes.
    
    Author: Rahul Nathan
"""

#Import Statements
import maya.cmds as cmds
import sys
from functools import partial

class CameraTools(object):
    """ Methods to create and control the attributes of the camera and imagePlane
    """
    def __init__(self):
        """ Initializes the UI, deletes window if it already exists.
        """
        self.camWindow = "Camera Tools"
        if cmds.window(self.camWindow, exists=True):
            cmds.deleteUI(self.camWindow)
            
        self.camWindow = cmds.window("Camera Tools")
        cmds.window(self.camWindow, edit=True, width=300, height=60, sizeable=False)
        
        self.createLayout()
   
    #====================================================================#
    # Create UI
    #====================================================================#
    def createLayout(self):
        """ Create the layout for the UI window.
        """
        mainLayout = cmds.columnLayout(width=300)
        cmds.separator()
        self.createCameraControlLayout(mainLayout)
        self.imagePlaneControlLayout(mainLayout)
        
    def createCameraControlLayout(self, mainLayout):
        """ Create Camera Attributes Control Layout.
            Args:
                mainLayout (cmds.columnLayout): Main Layout of the window.
        """
        camAttrLayout = cmds.frameLayout(
            width=300, 
            label="Camera Attributes Control", 
            collapse=True,
            collapsable=True, 
            marginWidth=5,
            parent=mainLayout,
            expandCommand=partial(self.frameCollapseChanged, str(mainLayout)),
            collapseCommand=partial(self.frameCollapseChanged, str(mainLayout))
        )
        cmds.separator(style="none")
        createCamButton = cmds.button(label="Create Camera", command='cmds.camera()')
        cmds.rowColumnLayout (numberOfColumns=2)

        self.horizAperture = cmds.floatFieldGrp(label="Horizontal Film Aperture", cal=[1, 'left'], cw2=[120,80], v1=1.417, precision=3)
        HA_button = cmds.button(label="Apply", command='self.setFieldValue("horizontalFilmAperture", self.horizAperture)')

        self.vertAperture = cmds.floatFieldGrp(l="Vertical Film Aperture", cal=[1, 'left'], cw2=[120,80], v1=0.945, precision=3)
        VA_button = cmds.button(label="Apply", command='self.setFieldValue("verticalFilmAperture", self.vertAperture)')

        self.focalLength = cmds.floatFieldGrp(label="Focal Length", cal=[1, 'left'], cw2=[120,80], v1=35)
        FL_button = cmds.button(label="Apply", command='self.setFieldValue("focalLength", self.focalLength)')

        self.nearClip = cmds.floatFieldGrp(label="Near Clip Plane", cal=[1, 'left'], cw2=[120,80], v1=0.1)
        NC_button = cmds.button(label="Apply", command='self.setFieldValue("nearClipPlane", self.nearClip)')

        self.farClip = cmds.floatFieldGrp(label="Far Clip Plane", cal=[1, 'left'], cw2=[120,80], v1=100000)
        FC_button = cmds.button(label="Apply", command='self.setFieldValue("farClipPlane", self.farClip)')

        cmds.setParent('..')

        cmds.text(label="Display Options:", font="boldLabelFont", align="left")
        cmds.columnLayout()
        self.filmGate = cmds.checkBox(
            label="Display Film Gate", 
            onc='self.setFieldValue("displayFilmGate", None, 1)', 
            ofc='self.setFieldValue("displayFilmGate", None, 0)'
        )
        self.resGate = cmds.checkBox(
            label="Display Resolution Gate", 
            onc='self.setFieldValue("displayResolution", None, 1)', 
            ofc='self.setFieldValue("displayResolution", None, 0)'
        )
        cmds.separator()
        cmds.setParent('..')
    
    def imagePlaneControlLayout(self, mainLayout):
        """ Create ImagePlane Attributes Control Layout.
            Args:
                mainLayout (cmds.columnLayout): Main Layout of the window.
        """
        ipAttrLayout = cmds.frameLayout(
            width=300, 
            label="ImagePlane Attributes Control", 
            collapse=True,
            collapsable=True, 
            marginWidth=5,
            parent=mainLayout,
            expandCommand=partial(frameCollapseChanged, str(mainLayout)),
            collapseCommand=partial(frameCollapseChanged, str(mainLayout))
        )
        cmds.separator(style="none")
        selectImgPlaneButton = cmds.button(label="Select all imagePlanes", command='self.selectImgPlaneFunc()')
        cmds.text(label="Display:", font="boldLabelFont", align="left")
        cmds.columnLayout()
        ipDisplay = cmds.radioButtonGrp(
            numberOfRadioButtons=2,
            l1="Looking through Camera",
            l2="In all views",
            cw2=[150,80],
            on1='self.lookThrough()',
            on2='self.allViews()'
        )
        cmds.separator()

        cmds.rowColumnLayout (numberOfColumns=2)
        self.alphaGain = cmds.floatFieldGrp(label="Alpha Gain", cal=[1, 'left'], cw2=[80,80], v1=1, precision=3)
        AG_button = cmds.button(label="Apply", command='self.setFieldValue("alphaGain", self.alphaGain)')
        cmds.setParent('..')
        cmds.separator()

        cmds.text(label="Placement:", font="boldLabelFont", align="left")
        cmds.rowColumnLayout (numberOfColumns=2)
        self.depth = cmds.floatFieldGrp(label="Depth", cal=[1, 'left'], cw2=[50,80], v1=100, precision=3)
        depth_button = cmds.button(label="Apply", command='self.setFieldValue("depth", self.depth)')
        cmds.setParent('..')

        cmds.rowColumnLayout (numberOfColumns=2)
        self.size = cmds.floatFieldGrp(label="Size", cal=[1, 'left'], nf=2, cw3=[50,80,80], v1=1.417, v2=0.945, precision=3)
        size_button = cmds.button(label="Apply", command='self.sizeFunc()')
        self.offset = cmds.floatFieldGrp(label="Offset", cal=[1, 'left'], nf=2, cw3=[50,80,80], v1=0, v2=0, precision=3)
        offset_button = cmds.button(label="Apply", command='self.offsetFunc()')

        cmds.rowColumnLayout (numberOfColumns=2)
        self.ipRotate = cmds.floatFieldGrp(label="Rotate", cal=[1, 'left'], cw2=[50,80], v1=0, precision=3)
        rotate_button = cmds.button(label="Apply", command='self.setFieldValue("rotate", self.ipRotate)')
        cmds.setParent('..')
        cmds.separator(style="none")
        cmds.setParent('..')

    def frameCollapseChanged(self, mainLayout):
        """ Function to dynamically resize the window based on the exapnded tabs.
            Args: 
                mainLayout (cmds.columnLayout): Main Layout of the window.
        """
        cmds.evalDeferred(
            "cmds.window('" + self.camWindow + "', e=1, h=sum(" \
                    "[ eval('cmds.' + cmds.objectTypeUI(child) + '(\\'' + child + '\\', query=1, h=1)')"\
                     "for child in cmds.columnLayout('" + mainLayout + "', query=1, childArray=1) ]"\
                ")"\
            ")"
        )
        
    def show(self):
        """ Show UI.
        """
        cmds.showWindow(self.camWindow)

    #====================================================================#
    # Utils
    #====================================================================#
    def findShapeSel(self):
        """ Find the shape attributes for the current selected objects.
            Returns:
                self.shapeSel (list): Shape attribute list.
        """
        sel= cmds.ls(sl=True)
        self.shapeSel=cmds.listRelatives(sel, s=True)

        return self.shapeSel

    def setFieldValue(self, attributeType, attributeName=None, attributeValue=None):
        """ Set the attribute value based on the field value from the UI.
            Args:
                attributeType (string): Type of attribute.
                attributeName (string): Name of the attribute in the UI.
                attributeValue (float): Value of the attribute in the UI.
        """
        if attributeValue == None:
            attributeValue = cmds.floatFieldGrp(attributeName, v1=True, q=True)

        self.shapeSel = self.findShapeSel()
        for each in self.shapeSel:
               cmds.setAttr('{0}.{1}'.format(each, attributeType), attributeValue)

    #----------------------------------------#
    # Image Plane Control Functions
    #----------------------------------------#
    def selectImgPlaneFunc(self):
        """ Selects all the imagePlanes in the scene.
        """
        selImgPlane = cmds.ls(type='imagePlane')
        cmds.select(selImgPlane)

    def lookThrough(self):
        """ Changes the imagePlane mode to "Look through Camera".
        """
        shapeSel = self.findShapeSel()
        for each in shapeSel:
            cmds.imagePlane(each, e=True, showInAllViews=False)
            cmds.select(cl=True)

    def allViews(self):
        """ Changes the imagePlane mode to "In all views".
        """
        shapeSel = self.findShapeSel()
        for each in shapeSel:
            cmds.imagePlane(each, e=True, showInAllViews=True)
            cmds.select(cl=True)

    def sizeFunc(self):
        """ Sets the Size values of the ImagePlane.
        """
        self.sizeVal1 = cmds.floatFieldGrp(self.size, v1=True, q=True)
        self.sizeVal2 = cmds.floatFieldGrp(self.size, v2=True, q=True)

        self.setFieldValue("sizeX", None, self.sizeVal1)
        self.setFieldValue("sizeY", None, self.sizeVal2)

    def offsetFunc(self):
        """ Sets the Offset values of the ImagePlane.
        """
        self.offsetVal1 = cmds.floatFieldGrp(self.offset, v1=True, q=True)
        self.offsetVal2 = cmds.floatFieldGrp(self.offset, v2=True, q=True)

        self.setFieldValue("sizeX", None, self.offsetVal1)
        self.setFieldValue("sizeY", None, self.offsetVal2)

#================================================================#
# Execution
#================================================================#
camTools = CameraTools()
camTools.show()

