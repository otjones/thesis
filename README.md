# Files

- **CATTMaterials.txt** Store the material properties and names, should correspond to names used in assetsLibrary.blend
- **assetsLibrary.blend** Blender file with materials, should be added to asset manager in main Blender project to enable drag and drop materials. Each geometry to be exported in the scene must have a material name which corresponds to one in the CATTMaterials.txt
- **dreamfactory-base.blend** Base model used for all simulations
- ***for-blender*** Code to run within Blender
- ***post-simulation*** Code torun on CATT simulation results files
- ***data-archive*** Zipped data for each experiment run in the paper. Includes all .GEO .SRC .REC files and all raw .txt CATT outputs and cleaned up .JSON stats files using post-simulation code. Also includes extra files where necessary including instructions files for post-simulation code to know which sources and recievers belong to which room.

# Code Summary

> Code is for experimental and research purposes only. Code requires editing and commenting to achieve its functions.

## For Blender

### blender-main.py

This script was written to be used as an add-on, and was run from Blender's text editor. In BLender, open a text editor window and paste the code. Edit the paramters at the top of the script and run. A UI panel will appear on the right hand side of the 3D viewport workspace with further prompts and two buttons.

- **Export:** Runs the export sequence to save to disk the .GEO .SRC and .REC files and the room configuration description files (if uncommented in code)
- **Build Instructions:** Exports .TXT files to describe which sources and recievers are in which room, using the bounding box empty.

### Scene setup

- **GEO** scene collection for all exportable geometry. Geometry should be clean with no overlapping vertices
- **SRC** scene collection for all exportable sound sources. Naming: S\_{source number}\_{directivity file}, e.g. "S_0_omni.SD0"
- **REC** scene collection for all exportable sound recievers. Naming: R\_{reciever number}, e.g. "R_0"
- **TAR** scene collection for all sound source target (used for source direction). Naming: T\_{source number}, e.g. "T_0"
- **BOUNDS** scene collection for bounding box empty object around the room. Naming: name of room, when exporting multiple rooms at once indices are appended.

### Code dependancies

Assets blend file and materials txt file must be in the _assets path_ set within the UI panel. Parts of the code will not run if any of the required inputs are missing, most major errors will be printed in the UI panel.

### blender-implement.py

Script to simply load an implementation json file and hide/show relavent panels. 

## Post Simulation

### ansis.py

Statistical analysis and chart plotting for sorted results

### blenderInfo.py

Static file to store panel - zone belongings

### compareSNR.py

Plots bar chart of the 16 candidate rooms optimised for SNR

### learn.py

Used for all optimisation and some analysis and chart plotting

### panels_det.py

Used to sort through the 42 simulation results testing each zone at a time and produce implementaton file

### plot_T30_histo.py

Plots histograms of random rooms results

### plotsummary.py

Plots final summary bar chart to compare methods

### presortINS.py

Generates instruction files for sortDS.py to use when converting raw .txt results from CATT into useful .json stats

###reduceSNR.py

Called from other scripts, used to calculate mean SNR of a room given its four src-rec pairs

###sortDS.py

Used to sort the raw .txt results files from CATT into usefl .JSON data files, which are used in all subsequent analysis

###t30test.py

Used to plot T30 convergence of optimised rooms
