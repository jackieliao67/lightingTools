"""
Create RGB ID shaders
"""

import maya.cmds as mc

def createIDshaders():
    #create shader list
    sgList = mc.ls(type = "shadingEngine")
    #create shader name
    redName = "ID_RED"
    greenName = "ID_GREEN"
    blueName = "ID_BLUE"
    blackName = "ID_BLACK"
    #create RED shader
    if redName+"SG" in sgList:
        connectList = mc.listConnections(redName+"SG")
        if redName in connectList:
            pass
        else:
            redShader = mc.shadingNode('surfaceShader', asShader = True, n = redName)
            redSG = redName+"SG"
            mc.connectAttr(redShader+".outColor", redSG+".surfaceShader", f = True)
            mc.setAttr(redShader+".outColor",1,0,0, type = "double3")
    else:
        redShader = mc.shadingNode('surfaceShader', asShader = True, n = redName)
        redSG = mc.sets(n = redShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
        mc.connectAttr(redShader+".outColor", redSG+".surfaceShader", f = True)
        mc.setAttr(redShader+".outColor",1,0,0, type = "double3")

    #create GREEN shader
    if greenName+"SG" in sgList:
        connectList = mc.listConnections(greenName+"SG")
        if greenName in connectList:
            pass
        else:
            greenShader = mc.shadingNode('surfaceShader', asShader = True, n = greenName)
            greenSG = greenName+"SG"
            mc.connectAttr(greenShader+".outColor", greenSG+".surfaceShader", f = True)
            mc.setAttr(greenShader+".outColor",0,1,0, type = "double3")
    else:
        greenShader = mc.shadingNode('surfaceShader', asShader = True, n = greenName)
        greenSG = mc.sets(n = greenShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
        mc.connectAttr(greenShader+".outColor", greenSG+".surfaceShader", f = True)
        mc.setAttr(greenShader+".outColor",0,1,0, type = "double3")

    #create BLUE shader
    if blueName+"SG" in sgList:
        connectList = mc.listConnections(blueName+"SG")
        if blueName in connectList:
            pass
        else:
            blueShader = mc.shadingNode('surfaceShader', asShader = True, n = blueName)
            blueSG = blueName+"SG"
            mc.connectAttr(blueShader+".outColor", blueSG+".surfaceShader", f = True)
            mc.setAttr(blueShader+".outColor",0,0,1, type = "double3")
    else:
        blueShader = mc.shadingNode('surfaceShader', asShader = True, n = blueName)
        blueSG = mc.sets(n = blueShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
        mc.connectAttr(blueShader+".outColor", blueSG+".surfaceShader", f = True)
        mc.setAttr(blueShader+".outColor",0,0,1, type = "double3")

    #create BLACK shader
    if blackName+"SG" in sgList:
        connectList = mc.listConnections(blackName+"SG")
        if blackName in connectList:
            pass
        else:
            blackShader = mc.shadingNode('surfaceShader', asShader = True, n = blackName)
            blackSG = blackName+"SG"
            mc.connectAttr(blackShader+".outColor", blackSG+".surfaceShader", f = True)
            mc.setAttr(blackShader+".outColor",0,0,0, type = "double3")
    else:
        blackShader = mc.shadingNode('surfaceShader', asShader = True, n = blackName)
        blackSG = mc.sets(n = blackShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
        mc.connectAttr(blackShader+".outColor", blackSG+".surfaceShader", f = True)
        mc.setAttr(blackShader+".outColor",0,0,0, type = "double3")
