from fbx import *
import sys, os

class animKey: 
    #Class that holds FbxTime and value pair for an animation keyframe
        def __init__(self, time, val):
            self.time = time
            self.val = val 
        def __str__(self):
            return "[" + str(self.time) + ": " + str(self.val) + "]"

class animChannel: 
    # Class that holds string and list of animKeys pair
    # animType can be "TX", "TY", "TZ", "RX", "RY", "RZ", "SX", "SY", "SZ"
    # "TX" means Translation X etc
        def __init__(self, animType, animKeys):
            self.animType = animType
            self.animKeys = animKeys 
        def __str__(self):
            result = self.animType + ", "
            for anim in self.animKeys:
                result = result + str(anim)
            return  result

class animNode:
    # Class that holds skeleton node name and list of animChannels
        def __init__(self, name, animChannels):
            self.name = name
            self.animChannels = animChannels 
        def __str__(self):
            result = "(" + self.name + ", "
            for anim in self.animChannels:
                result = result + str(anim)
            return  result + ")"

# Global variable to store the animation layers of the input FBX.
# Each element is a list of animNodes corresponding to an Animation Layer.
animLayers = []


def multAnims(mult): 
    # Multiplies the non-translation key values of the nodes listed in affectedNodes by mult.
    # This is just an example to edit the animation values stored in animLayers.

    # Replace the elements in the list below with the names of the nodes you want to multiply
    # the animations of in your of input fbx file.
    affectedNodes = ["mixamorig:Hips",
                    "mixamorig:Spine",
                    "mixamorig:Spine1",
                    "mixamorig:Spine2",
                    "mixamorig:Neck",
                    "mixamorig:Head",
                    "mixamorig:LeftUpLeg",
                    "mixamorig:RightUpLeg",]
    for layer in animLayers:
        for node in layer:
            if not node.name in affectedNodes: continue
            for channel in node.animChannels:
                if channel.animType[0] == "T": continue
                for key in channel.animKeys:
                    key.val = key.val*mult

def exportAnims(pScene,lSdkManager):
    # Creates a new fbx scene using the imported fbx file and the animation data stored in 
    # animLayers, which you may have edited. The new file will be "ExportedScene.fbx" in the
    # same directory as this code.
    import FbxCommon

    filepath = os.path.join(sys.path[0], "ExportedScene.fbx")
    layerN = len(animLayers)
    lAnimStack = pScene.GetSrcObject(FbxCriteria.ObjectType(FbxAnimStack.ClassId), 0)
    nbAnimLayers = lAnimStack.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimLayer.ClassId))
    # Disconnect the previous animation layer(s).
    for l in range(nbAnimLayers):
        lAnimLayer = lAnimStack.DisconnectSrcObject(lAnimStack.GetSrcObject(FbxCriteria.ObjectType(FbxAnimLayer.ClassId), l))
    # Create and add new animation layer(s) based on animLayers variable.
    for l in range(nbAnimLayers):
        lAnimLayer = FbxAnimLayer.Create(pScene, "Base Layer")
        lAnimStack.AddMember(lAnimLayer)
        fillLayer(pScene.GetRootNode(),lAnimLayer,l)
    FbxCommon.SaveScene(lSdkManager, pScene, filepath)

# Recursively create animations in the new animation layer based on the contents of animLayers[layerNo]
def fillLayer(pNode,pAnimLayer,layerNo):
    for nodes in animLayers[layerNo]:
        if nodes.name == pNode.GetName():
            node = nodes
       
    # Flags to check is a CurveNode for the given type of animation has already been created.
    translation = False
    rotation = False
    scaling = False

    for channel in node.animChannels:
        if channel.animType == "TX":
            if not translation:
                # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
                pNode.LclTranslation.GetCurveNode(pAnimLayer, True)
                translation = True

            lTime = FbxTime()
            lCurve = pNode.LclTranslation.GetCurve(pAnimLayer, "X", True)
            if lCurve:
                lCurve.KeyModifyBegin()
                for key in channel.animKeys:
                    lTime.SetSecondDouble(key.time.GetSecondDouble())
                    lKeyIndex = lCurve.KeyAdd(lTime)[0]
                    lCurve.KeySet(lKeyIndex, lTime, key.val)
                lCurve.KeyModifyEnd()

        elif channel.animType == "TY":
            if not translation:
                # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
                pNode.LclTranslation.GetCurveNode(pAnimLayer, True)
                translation = True
            lTime = FbxTime()
            lCurve = pNode.LclTranslation.GetCurve(pAnimLayer, "Y", True)
            if lCurve:
                lCurve.KeyModifyBegin()
                for key in channel.animKeys:
                    lTime.SetSecondDouble(key.time.GetSecondDouble())
                    lKeyIndex = lCurve.KeyAdd(lTime)[0]
                    lCurve.KeySet(lKeyIndex, lTime, key.val)
                lCurve.KeyModifyEnd()

        elif channel.animType == "TZ":
            if not translation:
                # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
                pNode.LclTranslation.GetCurveNode(pAnimLayer, True)
                translation = True
            lTime = FbxTime()
            lCurve = pNode.LclTranslation.GetCurve(pAnimLayer, "Z", True)
            if lCurve:
                lCurve.KeyModifyBegin()
                for key in channel.animKeys:
                    lTime.SetSecondDouble(key.time.GetSecondDouble())
                    lKeyIndex = lCurve.KeyAdd(lTime)[0]
                    lCurve.KeySet(lKeyIndex, lTime, key.val)
                lCurve.KeyModifyEnd()
        elif channel.animType == "RX":
            if not rotation:
                # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
                pNode.LclRotation.GetCurveNode(pAnimLayer, True)
                rotation = True
            lTime = FbxTime()
            lCurve = pNode.LclRotation.GetCurve(pAnimLayer, "X", True)
            if lCurve:
                lCurve.KeyModifyBegin()
                for key in channel.animKeys:
                    lTime.SetSecondDouble(key.time.GetSecondDouble())
                    lKeyIndex = lCurve.KeyAdd(lTime)[0]
                    lCurve.KeySet(lKeyIndex, lTime, key.val)
                lCurve.KeyModifyEnd()
        elif channel.animType == "RY":
            if not rotation:
                # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
                pNode.LclRotation.GetCurveNode(pAnimLayer, True)
                rotation = True
            lTime = FbxTime()
            lCurve = pNode.LclRotation.GetCurve(pAnimLayer, "Y", True)
            if lCurve:
                lCurve.KeyModifyBegin()
                for key in channel.animKeys:
                    lTime.SetSecondDouble(key.time.GetSecondDouble())
                    lKeyIndex = lCurve.KeyAdd(lTime)[0]
                    lCurve.KeySet(lKeyIndex, lTime, key.val)
                lCurve.KeyModifyEnd()
        elif channel.animType == "RZ":
            if not rotation:
                # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
                pNode.LclRotation.GetCurveNode(pAnimLayer, True)
                rotation = True
            lTime = FbxTime()
            lCurve = pNode.LclRotation.GetCurve(pAnimLayer, "Z", True)
            if lCurve:
                lCurve.KeyModifyBegin()
                for key in channel.animKeys:
                    lTime.SetSecondDouble(key.time.GetSecondDouble())
                    lKeyIndex = lCurve.KeyAdd(lTime)[0]
                    lCurve.KeySet(lKeyIndex, lTime, key.val)
                lCurve.KeyModifyEnd()
        elif channel.animType == "SX":
            if not scaling:
                # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
                pNode.LclScaling.GetCurveNode(pAnimLayer, True)
                scaling = True
            lTime = FbxTime()
            lCurve = pNode.LclScaling.GetCurve(pAnimLayer, "X", True)
            if lCurve:
                lCurve.KeyModifyBegin()
                for key in channel.animKeys:
                    lTime.SetSecondDouble(key.time.GetSecondDouble())
                    lKeyIndex = lCurve.KeyAdd(lTime)[0]
                    lCurve.KeySet(lKeyIndex, lTime, key.val)
                lCurve.KeyModifyEnd()
        elif channel.animType == "SY":
            if not scaling:
                # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
                pNode.LclScaling.GetCurveNode(pAnimLayer, True)
                scaling = True
            lTime = FbxTime()
            lCurve = pNode.LclScaling.GetCurve(pAnimLayer, "Y", True)
            if lCurve:
                lCurve.KeyModifyBegin()
                for key in channel.animKeys:
                    lTime.SetSecondDouble(key.time.GetSecondDouble())
                    lKeyIndex = lCurve.KeyAdd(lTime)[0]
                    lCurve.KeySet(lKeyIndex, lTime, key.val)
                lCurve.KeyModifyEnd()
        elif channel.animType == "SZ":
            if not scaling:
                # Create the CurveNode (it is necessary for the GetCurve to successfully allocate the Animation curve)
                pNode.LclScaling.GetCurveNode(pAnimLayer, True)
                scaling = True
            lTime = FbxTime()
            lCurve = pNode.LclScaling.GetCurve(pAnimLayer, "Z", True)
            if lCurve:
                lCurve.KeyModifyBegin()
                for key in channel.animKeys:
                    lTime.SetSecondDouble(key.time.GetSecondDouble())
                    lKeyIndex = lCurve.KeyAdd(lTime)[0]
                    lCurve.KeySet(lKeyIndex, lTime, key.val)
                lCurve.KeyModifyEnd()

    for lModelCount in range(pNode.GetChildCount()):
        fillLayer(pNode.GetChild(lModelCount),pAnimLayer,layerNo)

def EditAndExportAnimation(pScene,lSdkManager):

    #############################################
    # PLACE ANY CODE/NEW FUNCTION CALLS HERE
    # You can access the animation data stored in animLayers after ReadAnimation has been called.
    # Example: "multAnims(3)" to multiple some nodes' animation values.
    # This example multAnims function is implemented above.









    #############################################

    # Export the FBX with the new multiplied animations.
    exportAnims(pScene,lSdkManager)

def ReadAnimation(pScene):
    for i in range(pScene.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimStack.ClassId))):
        lAnimStack = pScene.GetSrcObject(FbxCriteria.ObjectType(FbxAnimStack.ClassId), i)
        
        lOutputString = "Animation Stack Name: "
        lOutputString += lAnimStack.GetName()
        lOutputString += "\n"
        print(lOutputString)

        ReadAnimationStack(lAnimStack, pScene.GetRootNode())

def ReadAnimationStack(pAnimStack, pNode):
    nbAnimLayers = pAnimStack.GetSrcObjectCount(FbxCriteria.ObjectType(FbxAnimLayer.ClassId))

    lOutputString = "No of AnimLayers: "
    lOutputString += str(nbAnimLayers)
    print(lOutputString)

    for l in range(nbAnimLayers):
        lAnimLayer = pAnimStack.GetSrcObject(FbxCriteria.ObjectType(FbxAnimLayer.ClassId), l)

        lOutputString = "AnimLayer "
        lOutputString += str(l)
        print(lOutputString)

        # Add list of nodes representing an animation layer to animLayers
        animLayers.append(ReadAnimationLayer(lAnimLayer, pNode, []))

# Returns a list of animNode's.
def ReadAnimationLayer(pAnimLayer, pNode, nodes):
    lOutputString = "     Node Name: "
    lOutputString += pNode.GetName()
    print(lOutputString)

    # Create animNode using the node name and the list of the channels in it.
    node = animNode(pNode.GetName(),ReadChannels(pNode, pAnimLayer, ReadCurveKeys))
    nodes.append(node)
    print

    for lModelCount in range(pNode.GetChildCount()):
        ReadAnimationLayer(pAnimLayer, pNode.GetChild(lModelCount), nodes)
    return nodes

# Returns a list of animChannel's.
def ReadChannels(pNode, pAnimLayer, ReadCurve):
    lAnimCurve = None
    channels = []

    lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, "X")
    if lAnimCurve:
        print("TX")
        # Add animChannel representing an animation channel to channels
        channels.append(animChannel("TX",ReadCurve(lAnimCurve)))
    lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, "Y")
    if lAnimCurve:
        print("TY")
        # Add animChannel representing an animation channel to channels
        channels.append(animChannel("TY",ReadCurve(lAnimCurve)))
    lAnimCurve = pNode.LclTranslation.GetCurve(pAnimLayer, "Z")
    if lAnimCurve:
        print("TZ")
        # Add animChannel representing an animation channel to channels
        channels.append(animChannel("TZ",ReadCurve(lAnimCurve)))

    lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, "X")
    if lAnimCurve:
        print("RX")
        # Add animChannel representing an animation channel to channels
        channels.append(animChannel("RX",ReadCurve(lAnimCurve)))
    lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, "Y")
    if lAnimCurve:
        print("RY")
        # Add animChannel representing an animation channel to channels
        channels.append(animChannel("RY",ReadCurve(lAnimCurve)))
    lAnimCurve = pNode.LclRotation.GetCurve(pAnimLayer, "Z")
    if lAnimCurve:
        print("RZ")
        # Add animChannel representing an animation channel to channels
        channels.append(animChannel("RZ",ReadCurve(lAnimCurve)))

    lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, "X")
    if lAnimCurve:
        print("SX")
        # Add animChannel representing an animation channel to channels
        channels.append(animChannel("SX",ReadCurve(lAnimCurve)))
    lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, "Y")
    if lAnimCurve:
        print("SY")
        # Add animChannel representing an animation channel to channels
        channels.append(animChannel("SY",ReadCurve(lAnimCurve)))
    lAnimCurve = pNode.LclScaling.GetCurve(pAnimLayer, "Z")
    if lAnimCurve:
        print("SZ")
        # Add animChannel representing an animation channel to channels
        channels.append(animChannel("SZ",ReadCurve(lAnimCurve)))

    return channels


# Returns a list of animKey's.
def ReadCurveKeys(pCurve):
    lKeyCount = pCurve.KeyGetCount()
    curve = []

    for lCount in range(lKeyCount):  
        lTimeString = ""
        lKeyValue = pCurve.KeyGetValue(lCount)
        lKeyTime  = pCurve.KeyGetTime(lCount)

        lOutputString = lKeyTime.GetTimeString(lTimeString)
        lOutputString += ":"
        lOutputString += str(lKeyValue)
        print(lOutputString)

        # Create an animKey for this keyframe and add it to curve
        curve.append(animKey(lKeyTime,lKeyValue))
    return curve