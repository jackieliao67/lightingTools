"""
Image Plane Creator
"""
import os
import shotgun
import maya.cmds as mc

def imgPlaneCreator():
    #get show, shot, asset, version
    showName = os.getenv('SHOW')
    shotName = os.getenv('SHOT')
    assetName = 'BG_light_flatanim_plate'
    highestVersion = shotgun.getLastVersion(showName, shotName, assetName)[assetName]
    if highestVersion == 0:
        #no light flatanim plate published, set starting path to lib/images
        startPath = '/X/projects/' + showName + '/SHOTS/' + shotName + '/lib/images'
    else:
        #get version name
        if len(str(highestVersion)) == 1:
            versionName = 'v00' + str(highestVersion)
        if len(str(highestVersion)) == 2:
            versionName = 'v0' + str(highestVersion)
        if len(str(highestVersion)) == 3:
            versionName = 'v' + str(highestVersion)
        #create starting path
        startPath = '/X/projects/' + showName + '/SHOTS/' + shotName + '/lib/images/anim/BG_flatanim_plate/' + assetName + '/' + versionName 
    #get render settings
    renderEngine = mc.getAttr("defaultRenderGlobals.ren")
    resWidth = mc.getAttr('defaultResolution.width')
    resHeight = mc.getAttr('defaultResolution.height')
    deviceAspectRatio = mc.getAttr('defaultResolution.deviceAspectRatio')
    #get selected panel
    activePanel = mc.getPanel(withFocus = True)
    if (mc.objectTypeUI(activePanel) == 'modelEditor'):
        #get camera
        activeCam = mc.modelPanel(activePanel, q = True, camera = True)
        camShape = mc.listRelatives(activeCam, shapes = True)
        #get camera info
        camScale = mc.getAttr(camShape[0]+'.cameraScale')
        camAperture = mc.getAttr(camShape[0]+'.horizontalFilmAperture')
        regSizeX = float(camAperture)
        regSizeY = float(camAperture) / float(deviceAspectRatio)
        newSizeX = regSizeX * float(camScale)
        newSizeY = regSizeY * float(camScale)
        #open file browser
        filePath = mc.fileDialog2(fileMode = 1, caption = 'Create Image Plane', dir = startPath)
        #create image plane and setup attributes
        if filePath:
            if (len(filePath) == 1):
                imgPlaneName = mc.imagePlane(camera = camShape[0], fileName = filePath[0])
                mc.setAttr(imgPlaneName[0]+'.useFrameExtension',1)
                mc.setAttr(imgPlaneName[0]+'.depth',5000)
                mc.setAttr(imgPlaneName[0]+'.fit',4)
                mc.setAttr(imgPlaneName[0]+'.coverageX',resWidth)
                mc.setAttr(imgPlaneName[0]+'.coverageY',resHeight)
                if renderEngine == "vray":
                    mc.setAttr(imgPlaneName[0]+'.sizeX',newSizeX)
                    mc.setAttr(imgPlaneName[0]+'.sizeY',newSizeY)
                else:
                    mc.setAttr(imgPlaneName[0]+'.sizeX',regSizeX)
                    mc.setAttr(imgPlaneName[0]+'.sizeY',regSizeY)
    else:
        mc.warning('Please select a view and try again.')







     
    
