# Code Summary

> Code is for experimental and research purposes only. Code requires editing and commenting to achieve its functions.

## For Blender

### blender-main.py

This script was written to be used as an add-on, and was run from Blender's text editor. In BLender, open a text editor window and paste the code. Edit the paramters at the top of the script and run. A UI panel will appear on the right hand side of the 3D viewport workspace with further prompts and two buttons.

- **Export:** Runs the export sequence to save to disk the .GEO .SRC and .REC files and the room configuration description files (if uncommented in code)
- **Build Instructions:** Exports .TXT files to describe which sources and recievers are in which room, using the bounding box empty.

### Scene setup and code dependancies

- GEO scene collection for all exportable geometry. Geometry should be clean with no overlapping vertices
- SRC scene collection for all exportable sound sources. Naming: S\_{source number}\_{directivity file}, e.g. "S_0_omni.SD0"
- REC scene collection for all exportable sound recievers. Naming: R\_{reciever number}, e.g. "R_0"
- TAR scene collection for all sound source target (used for source direction). Naming: T\_{source number}, e.g. "T_0"
- BOUNDS scene collection for bounding box empty object around the room. Naming: name of room, when exporting multiple rooms at once indices are appended.
