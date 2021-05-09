""" LIT AF
    Author: Rahul Nathan
    Description: Light Editor in Maya to create and edit lights in the Maya scene.
"""

import maya.cmds as cmds

window_name = 'lightEditorWindow'
window_title = 'LIT AF v1.3'
window_width = 300
window_height = 605

if (cmds.window(window_name, exists=True)):
    cmds.deleteUI(window_name, window=True)

lightEditorWindow = cmds.window(title = window_title, widthHeight = (window_width, window_height), sizeable=False)
cmds.columnLayout(adj=True)

#//////////Create Light Header//////////#
cmds.frameLayout(label="Lights", labelAlign='center', w=150)
cmds.separator( height=10, style='none' )
cmds.setParent('..')

#Create Lights UI#
cmds.rowColumnLayout( numberOfColumns=9, columnAlign=(1, 'right'), columnAttach=(2, 'both', 0), columnWidth= [(1,20),(9,20)] )
cmds.separator( height=10, style='none' )
cmds.shelfButton(label='Create ai Area Light', command='import mtoa.utils as mutils;mutils.createLocator("aiAreaLight", asLight=True)', annotation='ai Create Area Light', image='AreaLightShelf.png', style='iconOnly')
cmds.shelfButton(label='Create ai Mesh Light', command='import mtoa.utils as mutils; mutils.createMeshLight()', annotation='ai Create Mesh Light', image='MeshLightShelf.png', style='iconOnly')
cmds.shelfButton(label='Create ai Photometric Light', command='import mtoa.utils as mutils; mutils.createLocator("aiPhotometricLight", asLight=True)', annotation='ai Create Photometric Light', image='PhotometricLightShelf.png', style='iconOnly') 
cmds.shelfButton(label='Create ai SkyDome Light', command='import mtoa.utils as mutils; mutils.createLocator("aiSkyDomeLight", asLight=True)', annotation='ai Create SkyDome Light', image='SkydomeLightShelf.png', style='iconOnly')
cmds.shelfButton(label='Create ai Light Portal', command='import mtoa.ui.arnoldmenu as arnoldmenu; arnoldmenu.doCreateLightPortal()', annotation='ai Create Light Portal', image='LightPortalShelf.png', style='iconOnly')   
cmds.shelfButton(label='Create ai Sky', command='import mtoa.cmds.arnoldShelf as arnoldShelf; arnoldShelf.createSky()', annotation='ai Create Sky', image='SkyShelf.png', style='iconOnly')
cmds.shelfButton(label='Create ai Physical Sky', command='import mtoa.ui.arnoldmenu as arnoldmenu; arnoldmenu.doCreatePhysicalSky()', annotation='ai Create Physical Sky', image='PhysicalSkyShelf.png', style='iconOnly')
cmds.separator( height=10, style='none' )
cmds.separator( height=10, style='none' )
cmds.shelfButton(label='Create Ambient Light', command= cmds.ambientLight, annotation='Create Ambient Light', image='ambientlight.png', style='iconOnly')
cmds.shelfButton(label='Create Directional Light', command= cmds.directionalLight, annotation='Create Directional Light', image='directionallight.png', style='iconOnly')
cmds.shelfButton(label='Create Point Light', command= cmds.pointLight, annotation='Create Point Light', image='pointlight.png', style='iconOnly')
cmds.shelfButton(label='Create Spot Light', command= cmds.spotLight, annotation='Create Spot Light', image='spotlight.png', style='iconOnly')
cmds.shelfButton(label='Create Spot Light', command=lambda *args: cmds.CreateAreaLight(),annotation='Create Area Light', image1='arealight.png', style='iconOnly', )
cmds.separator( height=10, style='single' )
cmds.shelfButton(label='Create Camera', command= cmds.camera, annotation='Create camera', image='view.png', style='iconOnly')
cmds.setParent('..')
cmds.separator( height=5, style='double' )
cmds.separator( height=10, style='none' )

#Rename Lights UI#
cmds.rowColumnLayout( numberOfColumns=3, columnAlign=(1, 'right'), columnAttach=(2, 'both', 0), columnWidth=[(1, 60),(2,150),(3,60)] )
cmds.text(label= '   Name   ', align='right')
lightName=cmds.textField()
cmds.button(label = 'Rename', command = 'lightRename(lightName)')
cmds.setParent('..')
cmds.separator( height=10, style='none' )

#//////////Light Attributes Header//////////#
cmds.frameLayout(label="Light Attributes", labelAlign='center', w=150)
cmds.separator( height=10, style='none' )
cmds.setParent('..')

#Light Attributes UI#
cmds.rowColumnLayout( numberOfColumns=3, columnAlign=(1, 'right'), columnAttach=(2, 'both', 0), columnWidth=(2, 150) )

#Color UI#
cmds.text(label= '  Color  ', align='right')
lightColor=cmds.colorSliderGrp(rgb=(1, 1, 1),cal=(1,"right"),adj=True)
cmds.button(label = 'Apply', command = 'lightColorAtrribute(lightColor)')

#Intensity UI#
cmds.text(label= 'Intensity  ', align='right')
intensityInputField= cmds.floatField(value=1, precision=3)
cmds.button(label = 'Apply', command = 'intensityAttribute(intensityInputField)')

#Exposure UI#
cmds.text(label= '  Exposure  ', align='right')
exposureInputField= cmds.floatField(value=0, precision=3)
cmds.button(label = 'Apply', command = 'exposureAttribute(exposureInputField)')

#Spread UI#
cmds.text(label= '  Spread  ', align='right')
spreadInputField= cmds.floatField(minValue=0, maxValue=1,value=1, precision=3)
cmds.button(label = 'Apply', command = 'spreadAttribute(spreadInputField)')

#Roundness UI#
cmds.text(label= '  Roundness  ', align='right')
roundnessInputField= cmds.floatField(minValue=0, maxValue=1,value=0, precision=3)
cmds.button(label = 'Apply', command = 'roundnessAttribute(roundnessInputField)')

#Soft Edge UI#
cmds.text(label= '  Soft Edge  ', align='right')
softEdgeInputField= cmds.floatField(minValue=0, maxValue=1,value=0, precision=3)
cmds.button(label = 'Apply', command = 'softEdgeAttribute(softEdgeInputField)')

#Samples UI# 
cmds.text(label= '  Samples  ', align='right')
samplesInputField= cmds.intField(minValue=0, value=1)
cmds.button(label = 'Apply', command = 'samplesAttribute(samplesInputField)')

#Cast Shadows UI# 
cmds.separator( height=10, style='none' )
castShadowCheckBox = cmds.checkBox( label='Cast Shadows', value=1, align='center', offCommand='castShadowOff(castShadowCheckBox)', onCommand='castShadowOn(castShadowCheckBox)'  )
cmds.separator( height=10, style='none' )

#Shadow Density UI#
cmds.text(label= '  Shadow Density  ', align='right')
shadowDensityInputField= cmds.floatField(minValue=0, maxValue=1,value=1, precision=3)
cmds.button(label = 'Apply', command = 'shadowDensityAttribute(shadowDensityInputField)')

#Shadow Color UI#
cmds.text(label= '  Shadow Color  ', align='right')
shadowColor=cmds.colorSliderGrp(rgb=(0, 0, 0),cal=(1,"left"),adj=True)
cmds.button(label = 'Apply', command = 'shadowColorAtrribute(shadowColor)')

cmds.setParent('..')

#//////////Visbility Header//////////#
cmds.separator( height=10, style='double' )
cmds.frameLayout(label="Visibility",w=150)
cmds.separator( height=10, style='none' )
cmds.setParent('..')

#Visibility UI#
cmds.rowColumnLayout( numberOfColumns=3, columnAlign=(1, 'right'), columnAttach=(2, 'both', 0), columnWidth=(2, 150) )

#Diffuse UI#
cmds.text(label= '  Diffuse  ', align='right')
diffuseInputField= cmds.floatField(minValue=0, maxValue=1, value=1, precision=3)
cmds.button(label = 'Apply', command = 'diffuseVisibility(diffuseInputField)')

#Specular UI#
cmds.text(label= '  Specular  ', align='right')
specularInputField= cmds.floatField(minValue=0, maxValue=1, value=1, precision=3)
cmds.button(label = 'Apply', command = 'specularVisibility(specularInputField)')

#SSS UI#
cmds.text(label= '  SSS  ', align='right')
sssInputField= cmds.floatField(minValue=0, maxValue=1, value=1, precision=3)
cmds.button(label = 'Apply', command = 'sssVisibility(sssInputField)')

#Indirect UI#
cmds.text(label= '  Indirect  ', align='right')
indirectInputField= cmds.floatField(minValue=0, maxValue=1, value=1, precision=3)
cmds.button(label = 'Apply', command = 'indirectVisibility(indirectInputField)')

#Volume UI#
cmds.text(label= '  Volume ', align='right')
volumeInputField = cmds.floatField(minValue=0, maxValue=1, value=1, precision=3)
cmds.button(label = 'Apply', command = 'volumeVisibility(volumeInputField)')
cmds.setParent('..')

#End UI#
cmds.separator( height=10, style='none' )
cmds.button(label="Close", c="cmds.deleteUI(lightEditorWindow)")



cmds.showWindow(lightEditorWindow)

#////////////////////END OF UI////////////////////#


#Color Attribute Function#
def lightColorAtrribute(lightColor):
    sel = cmds.ls (sl = 1)
    queryLightColor= cmds.colorSliderGrp(lightColor, query=True, rgbValue= True)
    for each in sel:
         cmds.setAttr ( each + ('.colorR'),queryLightColor[0] )
         cmds.setAttr ( each + ('.colorG'),queryLightColor[1] )
         cmds.setAttr ( each + ('.colorB'),queryLightColor[2] )

#Intensity Attribute Function#
def intensityAttribute(intensityInputField):
    sel = cmds.ls (sl = 1)
    queryIntensityInputField= cmds.floatField(intensityInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.intensity'), queryIntensityInputField)
         
#Exposure Attribute Function#
def exposureAttribute(exposureInputField):
    sel = cmds.ls (sl = 1)
    queryExposureInputField= cmds.floatField(exposureInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiExposure'), queryExposureInputField)         
         
#Spread Attribute Function#
def spreadAttribute(spreadInputField):
    sel = cmds.ls (sl = 1)
    querySpreadInputField= cmds.floatField(spreadInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiSpread'), querySpreadInputField)  
            
#Roundness Attribute Function#
def roundnessAttribute(roundnessInputField):
    sel = cmds.ls (sl = 1)
    queryRoundnessInputField= cmds.floatField(roundnessInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiRoundness'), queryRoundnessInputField)  
         
#Soft Edge Attribute Function#
def softEdgeAttribute(softEdgeInputField):
    sel = cmds.ls (sl = 1)
    querySoftEdgeInputField= cmds.floatField(softEdgeInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiSoftEdge'), querySoftEdgeInputField)  
         
#Samples Attribute Function#
def samplesAttribute(samplesInputField):
    sel = cmds.ls (sl = 1)
    querySamplesInputField= cmds.intField(samplesInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiSamples'), querySamplesInputField)  
         
#Cast Shadows Attribute Function#
def castShadowOff(castShadowCheckBox):
    sel = cmds.ls (sl=1)         
    for each in sel:
        cmds.setAttr( each + ('.aiCastShadows'), 0)
        
def castShadowOn(castShadowCheckBox):
    sel = cmds.ls (sl=1)         
    for each in sel:
        cmds.setAttr( each + ('.aiCastShadows'), 1)        
         
#Shadow Density Attribute Function#
def shadowDensityAttribute(shadowDensityInputField):
    sel = cmds.ls (sl = 1)
    queryShadowDensityInputField= cmds.floatField(shadowDensityInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiShadowDensity'), queryShadowDensityInputField)        
         
#Shadow Color Attribute Function#
def shadowColorAtrribute(shadowColor):
    sel = cmds.ls (sl = 1)
    queryShadowColor= cmds.colorSliderGrp(shadowColor, query=True, rgbValue= True)
    for each in sel:
         cmds.setAttr ( each + ('.aiShadowColorR'),queryShadowColor[0] )
         cmds.setAttr ( each + ('.aiShadowColorG'),queryShadowColor[1] )
         cmds.setAttr ( each + ('.aiShadowColorB'),queryShadowColor[2] )
                               
                               
#Diffuse Visibility Function#
def diffuseVisibility(diffuseInputField):
    sel = cmds.ls (sl = 1)
    queryDiffuseInputField= cmds.floatField(diffuseInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiDiffuse'), queryDiffuseInputField)
         
#Specular Visibility Function#
def specularVisibility(specularInputField):
    sel = cmds.ls (sl = 1)
    querySpecularInputField= cmds.floatField(specularInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiSpecular'), querySpecularInputField)
                  
#SSS Visibility Function#
def sssVisibility(sssInputField):
    sel = cmds.ls (sl = 1)
    querySSSInputField= cmds.floatField(sssInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiSss'), querySSSInputField)   

#Indirect Visibility Function#
def indirectVisibility(indirectInputField):
    sel = cmds.ls (sl = 1)
    queryIndirectInputField= cmds.floatField(indirectInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiIndirect'), queryIndirectInputField)                                 

#Volume Visibility Function#
def volumeVisibility(volumeInputField):
    sel = cmds.ls (sl = 1)
    queryVolumeInputField= cmds.floatField(volumeInputField, query=True,value=True)
    for each in sel:
         cmds.setAttr ( each + ('.aiVolume'), queryVolumeInputField)
         
#Light Rename Function#        
def lightRename(lightName):
    sel = cmds.ls (sl = 1)   
    queryLightRename=cmds.textField(lightName, query= True, text=True)
    for each in sel:
        cmds.rename(each, queryLightRename)         
        
