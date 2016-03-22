"""
Script Name: matchRenderLayers
Version: v1.3
Creator: Jackie Liao
Latest Update: 06/21/2012

"""
import maya.cmds as mc

# globel attributes
srcObjSel=[]
trgObjSel=[]
srcCmpList=[]
trgCmpList=[]
srcTrList=[]
trgTrList=[]
srcGrp=[]
trgGrp=[]

actLayerList = []
currentLayer = []
sourceObj = []
targetObjs = []
sourceShape = []
targetShapes = []

srcPreText=[""]
srcSufText=[""]
trgPreText=[""]
trgSufText=[""]

allLayerList=[]
selLayerList=[]

"""
Get All Layers

"""
def getAllLayers(* args):
    allLayerList[:]=[]
    tmpLayerList=mc.ls(type="renderLayer")    
    for lyr in tmpLayerList:
        if lyr == "defaultRenderLayer":
            pass
        else:           
            allLayerList.append(lyr)

"""
Get Selected Layers

"""
def getSelectedLayers(* args):
    selLayerList[:]=[]
    #check all regular layers
    for v in range(len(allLayerList)):
        CBvalue=mc.checkBox("CB"+str(v),q=True,value=True)
        if CBvalue == 1:        
            selLayerList.append(allLayerList[v])
    # check default render layer        
    CBmasterValue=mc.checkBox("CB_master",q=True,value=True)
    if CBmasterValue ==1:
        selLayerList.append("defaultRenderLayer")

"""
Get Act Layer List

"""
def getLayers(* args):
    actLayerList[:]=[] 
    sel = mc.ls(sl=True,l=True)
    # check selections
    if not sel:
        raise RuntimeError, "There is nothing selected!" 
           
    elif len(sel) == 1:
        raise RuntimeError, "You must select source object and target object!" 
          
    else:
        sourceObjTmp=sel[0]
        targetObjsTmp=sel[1:]
        sourceShapeTmp=mc.listRelatives(sourceObjTmp,f=True)
        hrcNum= len(sourceObjTmp.split("|"))
        hrcName=sel
        layerList=mc.listConnections(hrcName[0],type="renderLayer")
        # check which layers contain the source object
        if not layerList:
            pass
        else:
            for layerName in layerList:
                if layerName in actLayerList:
                    pass
                else:
                    actLayerList.append(layerName)
           
        for x in range(hrcNum-2):
            childName=hrcName
            hrcName=mc.listRelatives(childName[0],p=True,f=True)
            
            layerList=mc.listConnections(hrcName[0],type="renderLayer")
            
            if not layerList:
                pass
            else:
                for layerName in layerList:
                    if layerName in actLayerList:
                        pass
                    else:
                        actLayerList.append(layerName)
    # check layers which is duplicated from default render layer
    for lyr in allLayerList:
        globalValue = mc.getAttr(lyr+".global")
        if globalValue > 0:
            if lyr not in actLayerList:
                actLayerList.append(lyr)
    # check default render layer            
    CBmasterValue=mc.checkBox("CB_master",q=True,value=True)
    if CBmasterValue ==1:
        actLayerList.append("defaultRenderLayer")
                 
    sourceObj.append(sourceObjTmp)
    sourceShape.append(sourceShapeTmp[0])
    for obj in targetObjsTmp:
        targetObjs.append(obj)
        targetShapeTmp=mc.listRelatives(obj,f=True)
        targetShapes.append(targetShapeTmp[0])
    
"""
Get Selection Objs

"""
def selectionDefiner(* args):
    #define prefix and suffix
    srcPrefix = mc.textFieldGrp("srcP",q=True,text=True)
    srcSuffix = mc.textFieldGrp("srcS",q=True,text=True)
    trgPrefix = mc.textFieldGrp("trgP",q=True,text=True)
    trgSuffix = mc.textFieldGrp("trgS",q=True,text=True)
    
    #get root names
    sel=mc.ls(sl=True,l=True)
    srcGrpName=sel[0]
    trgGrpName=sel[1]
    
    # get source compare list
    mc.select(srcGrpName,hierarchy=1)
    srcSpName=mc.ls(sl=True,g=True,l=True)
    srcTrName=mc.listRelatives(srcSpName,p=True,f=True)
    
    for srcTr in srcTrName:
        srcGrpSplit = srcGrpName.split("|")
        srcTrSplit = srcTr.split(srcGrpSplit[-1])        
        srcSplitList= srcTrSplit[-1].split("|")
        srcSplitFixedList=[]
        srcCombinedName=""
    
        for srcSplitName in srcSplitList:
            if len(srcSplitName) > 0:
                srcSplitName = "|" + (srcSplitName[len(srcPrefix):]).rstrip(srcSuffix)
                srcSplitFixedList.append(srcSplitName)
         
        for srcSize in range(0,len(srcSplitFixedList)):
            srcTmpName = srcSplitFixedList[srcSize]
            srcCombinedName += srcTmpName
            
        srcTrList.append(srcTr)        
        srcCmpList.append(srcCombinedName)
        
            
    # get target compare list    
    mc.select(trgGrpName,hierarchy=1)
    trgSpName=mc.ls(sl=True,g=True,l=True)
    trgTrName=mc.listRelatives(trgSpName,p=True,f=True)
    
    for trgTr in trgTrName:
        trgGrpSplit = trgGrpName.split("|")
        trgTrSplit = trgTr.split(trgGrpSplit[-1]) 
        trgSplitList= trgTrSplit[-1].split("|")
        trgSplitFixedList=[]
        trgCombinedName=""
    
        for trgSplitName in trgSplitList:
            if len(trgSplitName) > 0:
                trgSplitName = "|" + (trgSplitName[len(trgPrefix):]).rstrip(trgSuffix)
                trgSplitFixedList.append(trgSplitName)
         
        for v in range(0,len(trgSplitFixedList)):
            trgTmpName = trgSplitFixedList[v]
            trgCombinedName += trgTmpName
                    
        trgTrList.append(trgTr)        
        trgCmpList.append(trgCombinedName)
        srcGrp.append(srcGrpName)
        trgGrp.append(trgGrpName)
                                                                                
"""
Add objs into layers

"""
def addObjs(layerName):
    globalValue = mc.getAttr(layerName+".global")
    if globalValue == 0:     
        for target in targetObjs:
            mc.editRenderLayerMembers(layerName, target,noRecurse=True)
    else:
        pass
                    
"""
Transfer Shaders

"""
def shaderTransfer(* args):        
    matSGName = mc.listConnections(sourceShape, type = "shadingEngine")

    if not matSGName:
        pass
    else:       
        for target in targetObjs:
            mc.sets(target,e = 1, forceElement = matSGName[0])
        
"""
Transfer Layer Override

"""
def overrideTransfer(layerName):
    sourceObjSplit = sourceObj[0].split("|")
    sourceShapeSplit = sourceShape[0].split("|")                
    rawOverrides = mc.editRenderLayerAdjustment(layerName, query=True, layer=True )
    allOverrides = []
    if layerName == "defaultRenderLayer":
        pass
    else:    
        if rawOverrides == None:
            pass
        else:
            for x in rawOverrides:
                if "instObjGroup" in x:
                    pass
                elif x in allOverrides:
                    pass
                else:
                    allOverrides.append(x)
    
            for eachOverride in allOverrides:
                attrName=eachOverride.split(".")
                # match transform node overrides
                srcObjAttrCheck = mc.attributeQuery(attrName[-1],node=sourceObj[0],ex=True)
                if srcObjAttrCheck == True:            
                    if sourceObjSplit[-1]+"."+attrName[-1] in eachOverride:
                        for eachTarget in targetObjs:
                            mc.editRenderLayerAdjustment(eachTarget+"."+attrName[-1])
                            mc.copyAttr(sourceObj,eachTarget,values=True,attribute=[attrName[-1]])
                # match shape node overrides
                srcShapeAttrCheck = mc.attributeQuery(attrName[-1],node=sourceShape[0],ex=True)
                if srcShapeAttrCheck == True:
                    if sourceShapeSplit[-1]+"."+attrName[-1] in eachOverride:
                        attrType = mc.getAttr(eachOverride,type=True)                
                        if "float3" in attrType:
                            valueX = mc.getAttr(sourceShape[0]+"."+attrName[-1]+"X") 
                            valueY = mc.getAttr(sourceShape[0]+"."+attrName[-1]+"Y")
                            valueZ = mc.getAttr(sourceShape[0]+"."+attrName[-1]+"Z")                   
                            for eachShape in targetShapes:                                
                                mc.editRenderLayerAdjustment(eachShape+"."+attrName[-1])
                                mc.setAttr(eachShape+"."+attrName[-1]+"X",valueX)
                                mc.setAttr(eachShape+"."+attrName[-1]+"Y",valueY)
                                mc.setAttr(eachShape+"."+attrName[-1]+"Z",valueZ)
                        else:
                            value = mc.getAttr(sourceShape[0]+"."+attrName[-1])
                            for eachShape in targetShapes:
                                mc.editRenderLayerAdjustment(eachShape+"."+attrName[-1])
                                mc.setAttr(eachShape+"."+attrName[-1],value)
                                
"""
clear list

"""

def clearList(*args):
    srcObjSel[:]=[]
    trgObjSel[:]=[]
    srcCmpList[:]=[]
    trgCmpList[:]=[]
    srcTrList[:]=[]
    trgTrList[:]=[]
    srcGrp[:]=[]
    trgGrp[:]=[]
    sourceObj[:]= []
    targetObjs[:]= []
    sourceShape[:]= []
    targetShapes[:]= []
                           
"""
Define Buttons

"""
# Select All Button
def selectAllLayersButton(* args):
    for p in range(len(allLayerList)):
        mc.checkBox("CB"+str(p),edit=True,value=True)
    mc.checkBox("CB_master",edit=True,value=True)
# Deselect All Button       
def deselectAllLayersButton(* args):
    for r in range(len(allLayerList)):
        mc.checkBox("CB"+str(r),edit=True,value=False)
    mc.checkBox("CB_master",edit=True,value=False)
# Refresh Button        
def refreshButton(* args):
    if (mc.window("matchRenderLayers", ex = True)):
        srcPreText[0] = mc.textFieldGrp("srcP",q=True,text=True)
        srcSufText[0] = mc.textFieldGrp("srcS",q=True,text=True)
        trgPreText[0] = mc.textFieldGrp("trgP",q=True,text=True)
        trgSufText[0] = mc.textFieldGrp("trgS",q=True,text=True)
        
    matchRenderLayers()
# Match All Button in "Match By Selection" Section
def SELmatchAllButton(* args):
    clearList()
    currentLayer = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )
    getLayers()
    getSelectedLayers()
    for actLayer in actLayerList:
        for selLayer in selLayerList:
            if actLayer == selLayer:
                mc.editRenderLayerGlobals(currentRenderLayer=actLayer)   
                addObjs(actLayer)    
                shaderTransfer()
                overrideTransfer(actLayer)
    mc.editRenderLayerGlobals(currentRenderLayer=currentLayer)    
    
# Match Layers Button in "Match By Selection" Section
def SELmatchLayerButton(* args):
    clearList()
    currentLayer = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )
    getLayers()
    getSelectedLayers()
    for actLayer in actLayerList:
        for selLayer in selLayerList:
            if actLayer == selLayer:
                mc.editRenderLayerGlobals(currentRenderLayer=actLayer)   
                addObjs(actLayer)    
    mc.editRenderLayerGlobals(currentRenderLayer=currentLayer)
    
# Match Shaders Button in "Match By Selection" Section    
def SELmatchShaderButton(* args):
    clearList()
    currentLayer = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )
    getLayers()
    getSelectedLayers()  
    for actLayer in actLayerList:
        for selLayer in selLayerList:
            if actLayer == selLayer:
                mc.editRenderLayerGlobals(currentRenderLayer=actLayer)      
                shaderTransfer()
    mc.editRenderLayerGlobals(currentRenderLayer=currentLayer)
    
# Match Overrides Button in "Match By Selection" Section    
def SELmatchOverrideButton(* args):
    clearList()
    currentLayer = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )
    getLayers()
    getSelectedLayers()
    for actLayer in actLayerList:
        for selLayer in selLayerList:
            if actLayer == selLayer:
                mc.editRenderLayerGlobals(currentRenderLayer=actLayer)   
                overrideTransfer(actLayer)
    mc.editRenderLayerGlobals(currentRenderLayer=currentLayer)
        
# Match All Button in "Match By Name and Hierarchy" Section
def NAMEmatchAllButton(* args):
    clearList()
    currentLayer = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )
    selectionDefiner()
    for trgCt in range(len(trgCmpList)):
        for srcCt in range(len(srcCmpList)):
            if trgCmpList[trgCt] == srcCmpList[srcCt]:
                srcObjSel = srcTrList[srcCt]
                trgObjSel = trgTrList[trgCt]
                mc.select(srcObjSel,replace=True)
                mc.select(trgObjSel,add=True)
                getLayers()
                getSelectedLayers()
                for actLayer in actLayerList:
                    for selLayer in selLayerList:
                        if actLayer == selLayer:
                            mc.editRenderLayerGlobals(currentRenderLayer=actLayer)   
                            addObjs(actLayer)    
                            shaderTransfer()
                            overrideTransfer(actLayer)
                                                    
                actLayerList[:]=[]
                selLayerList[:]=[]
                sourceObj[:]=[]
                targetObjs[:]=[]
                sourceShape[:]=[]
                targetShapes[:]=[] 
                     
        if trgCmpList[trgCt] not in srcCmpList:
            print trgTrList[trgCt] + " doesn't match! "

    mc.select(srcGrp,replace=True)
    mc.select(trgGrp,add=True)        
            
    mc.editRenderLayerGlobals(currentRenderLayer=currentLayer)
# Match Layers Button in "Match By Name and Hierarchy" Section    
def NAMEmatchLayerButton(* args):
    clearList() 
    currentLayer = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )
    selectionDefiner()
    for trgCt in range(len(trgCmpList)):
        for srcCt in range(len(srcCmpList)):
            if trgCmpList[trgCt] == srcCmpList[srcCt]:
                srcObjSel = srcTrList[srcCt]
                trgObjSel = trgTrList[trgCt]
                mc.select(srcObjSel,replace=True)
                mc.select(trgObjSel,add=True)
                getLayers()
                getSelectedLayers()
                for actLayer in actLayerList:
                    for selLayer in selLayerList:
                        if actLayer == selLayer:
                            mc.editRenderLayerGlobals(currentRenderLayer=actLayer)   
                            addObjs(actLayer)    
                                                    
                actLayerList[:]=[]
                selLayerList[:]=[]
                sourceObj[:]=[]
                targetObjs[:]=[]
                sourceShape[:]=[]
                targetShapes[:]=[] 
                     
        if trgCmpList[trgCt] not in srcCmpList:
            print trgTrList[trgCt] + " doesn't match! "
            
    mc.select(srcGrp,replace=True)
    mc.select(trgGrp,add=True)       
            
    mc.editRenderLayerGlobals(currentRenderLayer=currentLayer)     
# Match Shaders Button in "Match By Name and Hierarchy" Section
def NAMEmatchShaderButton(* args):
    clearList()
    currentLayer = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )
    selectionDefiner()
    for trgCt in range(len(trgCmpList)):
        for srcCt in range(len(srcCmpList)):
            if trgCmpList[trgCt] == srcCmpList[srcCt]:
                srcObjSel = srcTrList[srcCt]
                trgObjSel = trgTrList[trgCt]
                mc.select(srcObjSel,replace=True)
                mc.select(trgObjSel,add=True)
                getLayers()
                getSelectedLayers()
                for actLayer in actLayerList:
                    for selLayer in selLayerList:
                        if actLayer == selLayer:
                            mc.editRenderLayerGlobals(currentRenderLayer=actLayer)       
                            shaderTransfer()
                                                    
                actLayerList[:]=[]
                selLayerList[:]=[]
                sourceObj[:]=[]
                targetObjs[:]=[]
                sourceShape[:]=[]
                targetShapes[:]=[] 
                     
        if trgCmpList[trgCt] not in srcCmpList:
            print trgTrList[trgCt] + " doesn't match! "
            
    mc.select(srcGrp,replace=True)
    mc.select(trgGrp,add=True)        
            
    mc.editRenderLayerGlobals(currentRenderLayer=currentLayer) 
# Match Overrides Button in "Match By Name and Hierarchy" Section
def NAMEmatchOverrideButton(* args):
    clearList() 
    currentLayer = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )
    selectionDefiner()
    for trgCt in range(len(trgCmpList)):
        for srcCt in range(len(srcCmpList)):
            if trgCmpList[trgCt] == srcCmpList[srcCt]:
                srcObjSel = srcTrList[srcCt]
                trgObjSel = trgTrList[trgCt]
                mc.select(srcObjSel,replace=True)
                mc.select(trgObjSel,add=True)
                getLayers()
                getSelectedLayers()
                for actLayer in actLayerList:
                    for selLayer in selLayerList:
                        if actLayer == selLayer:
                            mc.editRenderLayerGlobals(currentRenderLayer=actLayer)   
                            overrideTransfer(actLayer)
                                                    
                actLayerList[:]=[]
                selLayerList[:]=[]
                sourceObj[:]=[]
                targetObjs[:]=[]
                sourceShape[:]=[]
                targetShapes[:]=[] 
                     
        if trgCmpList[trgCt] not in srcCmpList:
            print trgTrList[trgCt] + " doesn't match! "
            
    mc.select(srcGrp,replace=True)
    mc.select(trgGrp,add=True)       
            
    mc.editRenderLayerGlobals(currentRenderLayer=currentLayer) 
           
"""
Creat GUI

"""
def matchRenderLayers(* args):
    getAllLayers()
    
    #define colors
    mainBgColor = (.2,.2,.2)
    firstTabColor = (.45,.15,.15)
    secondTabColor = (.1,.2,.5)
    thirdTabColor = (.15,.35,.1)
    buttonBgColor = (.32,.32,.32)
    
    #creating window
    if (mc.window("matchRenderLayers", ex = True)):
        mc.deleteUI("matchRenderLayers")
    mc.window("matchRenderLayers",w=360,h=600,t="matchRenderLayers",sizeable=True,titleBar=True, bgc=mainBgColor)
    mc.columnLayout()
    # "Select Layers" Section
    mc.frameLayout(label="SELECT LAYERS YOU WANT TO MATCH",collapsable=True,borderStyle="etchedIn",bgc=firstTabColor) 
    mc.rowColumnLayout(cw=(1,360))
    mc.gridLayout(cw=120,nc=3)
    mc.checkBox("CB_master",label="masterLayer",value=True)
    for x in range(len(allLayerList)):
        checkBoxName="CB"+str(x)
        mc.checkBox(checkBoxName,label=allLayerList[x],value=True)        
    mc.setParent('..')
    mc.rowLayout(numberOfColumns=3,w=360,cw3=(120,120,120),cl3=("center","center","center"))
    mc.button(label="Select All",c=selectAllLayersButton,w=100,bgc=buttonBgColor)
    mc.button(label="Deselect All",c=deselectAllLayersButton,w=100,bgc=buttonBgColor)
    mc.button(label="Refresh",c=refreshButton,w=100,bgc=buttonBgColor)
    mc.setParent('..') 
    mc.setParent('..')
    # "Match by Selection" Section
    mc.frameLayout(label="MATCH BY SELECTION",collapsable=True,borderStyle="etchedIn",bgc=secondTabColor) 
    mc.rowColumnLayout(cw=(1,360))       
    mc.separator("SEL_Tsep1", style = "none", h = 10)
    mc.text(label="Usage:", align="left")
    mc.separator("SEL_Tsep2", style = "none", h = 5)
    mc.text(label=" - Select SOURCE GEOMETRY (Only one)", align="left")
    mc.text(label=" - Select all TARGET GEOMETRIES (Could be multiple)", align="left")
    mc.text(label=" - Click the button to match.", align="left")
    mc.separator("SEL_Tsep3", style = "none", h = 5)
    mc.text(label="* Important Notes *", align="left")
    mc.separator("SEL_Tsep4", style = "none", h = 5)
    mc.text(label=" - Naming for SOURCE and TARGET doesn't matter in this section.", align="left")
    mc.text(label=" - Please select GEOMETRIES, no GROUPS.", align="left")
    mc.separator("SEL_Bsep1", style = "none", h = 10)
    mc.button("SEL_matchAll", label = "Match All", al = "center", h = 25, c = SELmatchAllButton, ann = "Match Layers,Shaders and Overrides by Selections",bgc=buttonBgColor)
    mc.separator("SEL_Bsep2", style = "none", h = 10)
    mc.button("SEL_matchLayer", label = "Match Layers", al = "center", h = 25, c = SELmatchLayerButton, ann = "Match Layers Only by Selections",bgc=buttonBgColor)
    mc.separator("SEL_Bsep3", style = "none", h = 10)
    mc.button("SEL_matchShader", label = "Match Shaders", al = "center", h = 25, c = SELmatchShaderButton, ann = "Match Shaders Only by Selections",bgc=buttonBgColor)
    mc.separator("SEL_Bsep4", style = "none", h = 10)
    mc.button("SEL_matchOverride", label = "Match Overrides", al = "center", h = 25, c = SELmatchOverrideButton, ann = "Match Overrides Only by Selections",bgc=buttonBgColor)
    mc.separator("SEL_Bsep5", style = "none", h = 10)
    mc.setParent("..")
    mc.setParent("..")
    # "Match by Name and Hierarchy" Section
    mc.frameLayout(label="MATCH BY NAME AND HIERARCHY",collapsable=True,borderStyle="etchedIn",bgc=thirdTabColor)
    mc.rowColumnLayout(cw=(1,360)) 
    mc.separator("NAME_Tsep1", style = "none", h = 15)
    mc.text(label="Usage:", align="left")
    mc.separator("NAME_Tsep2", style = "none", h = 5)
    mc.text(label=" - Select SOURCE and TARGET ROOT NODES", align="left")
    mc.text(label=" - Type in prefix or suffix if there is any", align="left")
    mc.text(label=" - Click the button to match.", align="left")
    mc.separator("NAME_Tsep3", style = "none", h = 15)
    mc.text(label="* Important Notes *", align="left")
    mc.separator("NAME_Tsep4", style = "none", h = 5)
    mc.text(label=" - SOURCE and TARGET must have the same ", align="left")
    mc.text(label="   Hierarchy and Naming Convention", align="left")
    mc.separator("NAME_Tsep5", style = "none", h = 15)
    mc.textFieldGrp("srcP",label="  Source Prefix  ", text=srcPreText[0],cw2=(80,270),cl2=("left","left"))
    mc.textFieldGrp("srcS",label="  Source Suffix  ", text=srcSufText[0],cw2=(80,270),cl2=("left","left"))
    mc.textFieldGrp("trgP",label="  Target Prefix  ", text=trgPreText[0],cw2=(80,270),cl2=("left","left"))
    mc.textFieldGrp("trgS",label="  Target Suffix  ", text=trgSufText[0],cw2=(80,270),cl2=("left","left"))
    mc.separator("NAME_Bsep1", style = "none", h = 10)
    mc.button("NAME_matchAll", label = "Match All", al = "center", h = 25, c = NAMEmatchAllButton, ann = "Match Layers,Shaders and Overrides",bgc=buttonBgColor)
    mc.separator("NAME_Bsep2", style = "none", h = 10)
    mc.button("NAME_matchLayer", label = "Match Layers", al = "center", h = 25, c = NAMEmatchLayerButton, ann = "Match Layers Only",bgc=buttonBgColor)
    mc.separator("NAME_Bsep3", style = "none", h = 10)
    mc.button("NAME_matchShader", label = "Match Shaders", al = "center", h = 25, c = NAMEmatchShaderButton, ann = "Match Shaders Only",bgc=buttonBgColor)
    mc.separator("NAME_Bsep4", style = "none", h = 10)
    mc.button("NAME_matchOverride", label = "Match Overrides", al = "center", h = 25, c = NAMEmatchOverrideButton, ann = "Match Overrides Only",bgc=buttonBgColor)
    mc.separator("NAME_Bsep5", style = "none", h = 10)
    mc.showWindow()

      

