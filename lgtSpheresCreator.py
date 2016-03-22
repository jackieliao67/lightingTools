"""
Lighting Spheres Creator
Version : v1.0
"""

import maya.cmds as mc

def lgtSpheresCreator():
    #check render engine
    renderEngine = mc.getAttr("defaultRenderGlobals.ren")

    #create locator
    loc = mc.spaceLocator(n = "Lgt_Spheres_"+str(renderEngine), p = (0,0,0))

    #create chromn ball
    chromnBallName = mc.polySphere(n = loc[0]+"_chromnBall")
    mc.delete(chromnBallName,ch = True)
    chromnBallShape = mc.listRelatives(chromnBallName[0], s = True)
    mc.setAttr(chromnBallShape[0]+'.castsShadows', 0)
    mc.setAttr(chromnBallShape[0]+'.receiveShadows', 0)
    mc.setAttr(chromnBallShape[0]+'.visibleInReflections', 0)
    mc.setAttr(chromnBallShape[0]+'.visibleInRefractions', 0)
    mc.setAttr(chromnBallName[0]+'.translateY', 7)
    mc.parent(chromnBallName[0], loc[0], relative = True)
    chromnBall = mc.ls(chromnBallName[0], l = True)

    #create gray ball
    grayBallName = mc.polySphere(n = loc[0]+"_grayBall")
    mc.delete(grayBallName,ch = True)
    grayBallShape = mc.listRelatives(grayBallName[0], s = True)
    mc.setAttr(grayBallShape[0]+'.castsShadows', 0)
    mc.setAttr(grayBallShape[0]+'.receiveShadows', 0)
    mc.setAttr(grayBallShape[0]+'.visibleInReflections', 0)
    mc.setAttr(grayBallShape[0]+'.visibleInRefractions', 0)
    mc.setAttr(grayBallName[0]+'.translateY', 4.5)
    mc.parent(grayBallName[0], loc[0], relative = True)
    grayBall = mc.ls(grayBallName[0], l = True)

    #create white ball
    whiteBallName = mc.polySphere(n = loc[0]+"_whiteBall")
    mc.delete(whiteBallName,ch = True)
    whiteBallShape = mc.listRelatives(whiteBallName[0], s = True)
    mc.setAttr(whiteBallShape[0]+'.castsShadows', 0)
    mc.setAttr(whiteBallShape[0]+'.receiveShadows', 0)
    mc.setAttr(whiteBallShape[0]+'.visibleInReflections', 0)
    mc.setAttr(whiteBallShape[0]+'.visibleInRefractions', 0)
    mc.setAttr(whiteBallName[0]+'.translateY', 2)
    mc.parent(whiteBallName[0], loc[0], relative = True)
    whiteBall = mc.ls(whiteBallName[0], l = True)
    
    #create and assign shaders by render engine 
    if renderEngine == "vray":
        assignVrayShaders(chromnBall,grayBall,whiteBall)
        mc.select(loc, r=True)
    elif renderEngine == "arnold":
        assignArnoldShaders(chromnBall,grayBall,whiteBall)
        mc.select(loc, r=True)
    else:
        assignMayaShaders(chromnBall,grayBall,whiteBall)
        mc.select(loc, r=True)
    
  
def assignVrayShaders(chromnBall,grayBall,whiteBall):
    #create and assign chromn ball shader
    chromnBallShader = mc.shadingNode('VRayMtl', asShader = True, n = "mat_chromnBall")
    chromnBallSG = mc.sets(n = chromnBallShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
    mc.connectAttr(chromnBallShader+".outColor", chromnBallSG+".surfaceShader", f = True)
    mc.setAttr(chromnBallShader+".color",0,0,0, type = "double3")
    mc.setAttr(chromnBallShader+".diffuseColorAmount",0)
    mc.setAttr(chromnBallShader+".reflectionColor",1,1,1,type = "double3")
    mc.setAttr(chromnBallShader+".refractionIOR",15)
    mc.sets(chromnBall,e = True, forceElement = chromnBallSG)
        
    #create and assign gray ball shader
    grayBallShader = mc.shadingNode('VRayMtl', asShader = True, n = "mat_grayBall")
    grayBallSG = mc.sets(n = grayBallShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
    mc.connectAttr(grayBallShader+".outColor", grayBallSG+".surfaceShader", f = True)
    mc.setAttr(grayBallShader+".color",0.18,0.18,0.18, type = "double3")
    mc.setAttr(grayBallShader+".reflectionColorAmount",0)
    mc.sets(grayBall,e = True, forceElement = grayBallSG)
    
    #create and assign white ball shader
    whiteBallShader = mc.shadingNode('VRayMtl', asShader = True, n = "mat_whiteBall")
    whiteBallSG = mc.sets(n = whiteBallShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
    mc.connectAttr(whiteBallShader+".outColor", whiteBallSG+".surfaceShader", f = True)
    mc.setAttr(whiteBallShader+".color",1,1,1, type = "double3")
    mc.setAttr(whiteBallShader+".reflectionColorAmount",0)
    mc.sets(whiteBall,e = True, forceElement = whiteBallSG)

    
def assignArnoldShaders(chromnBall,grayBall,whiteBall):
    #create and assign chromn ball shader
    chromnBallShader = mc.shadingNode('aiStandard', asShader = True, n = "mat_chromnBall")
    chromnBallSG = mc.sets(n = chromnBallShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
    mc.connectAttr(chromnBallShader+".outColor", chromnBallSG+".surfaceShader", f = True)
    mc.setAttr(chromnBallShader+".color",0,0,0, type = "double3")
    mc.setAttr(chromnBallShader+".Kd",0)
    mc.setAttr(chromnBallShader+".Ks",1)
    mc.setAttr(chromnBallShader+".specularRoughness",0)
    mc.sets(chromnBall,e = True, forceElement = chromnBallSG)
        
    #create and assign gray ball shader
    grayBallShader = mc.shadingNode('aiStandard', asShader = True, n = "mat_grayBall")
    grayBallSG = mc.sets(n = grayBallShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
    mc.connectAttr(grayBallShader+".outColor", grayBallSG+".surfaceShader", f = True)
    mc.setAttr(grayBallShader+".color",0.18,0.18,0.18, type = "double3")
    mc.setAttr(grayBallShader+".Kd",1)
    mc.setAttr(grayBallShader+".KsColor",0,0,0, type = "double3")
    mc.setAttr(grayBallShader+".Ks",0)
    mc.setAttr(chromnBallShader+".specularRoughness",0)
    mc.sets(grayBall,e = True, forceElement = grayBallSG)
    
    #create and assign white ball shader
    whiteBallShader = mc.shadingNode('aiStandard', asShader = True, n = "mat_whiteBall")
    whiteBallSG = mc.sets(n = whiteBallShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
    mc.connectAttr(whiteBallShader+".outColor", whiteBallSG+".surfaceShader", f = True)
    mc.setAttr(whiteBallShader+".color",1,1,1, type = "double3")
    mc.setAttr(whiteBallShader+".Kd",1)
    mc.setAttr(whiteBallShader+".KsColor",0,0,0, type = "double3")
    mc.setAttr(whiteBallShader+".Ks",0)
    mc.setAttr(chromnBallShader+".specularRoughness",0)
    mc.sets(whiteBall,e = True, forceElement = whiteBallSG)

        
def assignMayaShaders(chromnBall,grayBall,whiteBall):
    #create and assign chromn ball shader
    chromnBallShader = mc.shadingNode('blinn', asShader = True, n = "mat_chromnBall")
    chromnBallSG = mc.sets(n = chromnBallShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
    mc.connectAttr(chromnBallShader+".outColor", chromnBallSG+".surfaceShader", f = True)
    mc.setAttr(chromnBallShader+".color",0,0,0, type = "double3")
    mc.setAttr(chromnBallShader+".diffuse",0)
    mc.setAttr(chromnBallShader+".specularColor",1,1,1,type = "double3")
    mc.setAttr(chromnBallShader+".reflectivity",1)
    mc.setAttr(chromnBallShader+".eccentricity",0)
    mc.setAttr(chromnBallShader+".specularRollOff",1)
    mc.sets(chromnBall,e = True, forceElement = chromnBallSG)

    #create and assign gray ball shader
    grayBallShader = mc.shadingNode('lambert', asShader = True, n = "mat_grayBall")
    grayBallSG = mc.sets(n = grayBallShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
    mc.connectAttr(grayBallShader+".outColor", grayBallSG+".surfaceShader", f = True)
    mc.setAttr(grayBallShader+".color",0.18,0.18,0.18, type = "double3")
    mc.setAttr(grayBallShader+".diffuse",1)
    mc.sets(grayBall,e = True, forceElement = grayBallSG)

    #create and assign white ball shader
    whiteBallShader = mc.shadingNode('lambert', asShader = True, n = "mat_whiteBall")
    whiteBallSG = mc.sets(n = whiteBallShader + "SG", renderable = True, noSurfaceShader = True, empty = True)
    mc.connectAttr(whiteBallShader+".outColor", whiteBallSG+".surfaceShader", f = True)
    mc.setAttr(whiteBallShader+".diffuse",1)
    mc.setAttr(whiteBallShader+".color",1,1,1, type = "double3")
    mc.sets(whiteBall,e = True, forceElement = whiteBallSG)
