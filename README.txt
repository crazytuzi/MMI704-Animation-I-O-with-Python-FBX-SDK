ImportScene.py is the main Python file to run, Animation.py is only used by it to import/export FBX files and save/edit their animation data.
Code to edit animation data can be added in Animation.py/EditAndExportAnims function, as this is only a template. 
Jogging.fbx is the example input FBX.

When run, ImportScene.py will produce ExportedScene.fbx with the output FBX file, and output.txt containing the print output of the code.
The print output of the code contains all the ORIGINAL animation data under each Node, is only here for debug purposes/seeing the animation node names.

The code requires Autodesk Python FBX SDK to be installed in order to run. Recommended Python version: 3.7
