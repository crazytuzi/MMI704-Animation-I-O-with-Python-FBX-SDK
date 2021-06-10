import sys, os
from FbxCommon import *
from Animation import ReadAnimation, EditAndExportAnimation

if __name__ == "__main__":
    
    inputFbxFilename = "Jogging.fbx" # Example input 
    #Change this to the name of your input placed in the same directory as this code.

    sys.stdout = open(os.path.join(sys.path[0], "output.txt"), 'w')  
    lSdkManager, lScene = InitializeSdkObjects() # Prepare the FBX SDK.
    lResult = LoadScene(lSdkManager, lScene, os.path.join(sys.path[0], inputFbxFilename)) # Load the scene.

    if not lResult:
        print("\n\nAn error occurred while loading the scene...")
    else :

        ReadAnimation(lScene)
        EditAndExportAnimation(lScene,lSdkManager)

    lSdkManager.Destroy()
    sys.stdout.close()
    sys.exit(0)
