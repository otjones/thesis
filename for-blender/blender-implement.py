import bpy
import json
import os

best_log = "C:/Users/otjon/Documents/Imperial/Masters/Project/DREAMFACTORY/ARCHIVE/CONVERG-LOG/IMPLEMENTATION/panel_implementation_500_7.json"
best_lin = "C:/Users/otjon/Documents/Imperial/Masters/Project/DREAMFACTORY/ARCHIVE/CONVERG-LIN/IMPLEMENTATION/panel_implementation_1000_4.json"
best_det = "C:/Users/otjon/Documents/Imperial/Masters/Project/DREAMFACTORY/panel_implementation_det.json"
best_multi = "C:/Users/otjon/Documents/Imperial/Masters/Project/DREAMFACTORY/ARCHIVE/MULTI2-VAL/IMPLEMENTATION/panel_implementation_0_3.json"

for obj in bpy.data.collections["GEO"].objects:
    if "Baffle" in obj.name:
        bpy.data.collections["GEO"].objects[obj.name].hide_viewport = True

with open(best_multi, "r") as f:
    panel_dictionary = json.load(f)
    
print(panel_dictionary)

count = 0
for p in panel_dictionary:
    if "absorber" in p:
        if panel_dictionary[p] == True:
            count+=1
        bpy.data.collections["GEO"].objects[p].hide_viewport = not panel_dictionary[p]
    
    if "Baffle" in p:
        print(panel_dictionary[p])
        if panel_dictionary[p][0] > 0:
            print("Baffles")
            bpy.data.collections["GEO"].objects[p].hide_viewport = False
            bpy.data.collections["GEO"].objects[p].modifiers["Array"].count = panel_dictionary[p][0]
            bpy.data.collections["GEO"].objects[p].modifiers["Array"].relative_offset_displace[1] = panel_dictionary[p][1]
            count += panel_dictionary[p][0]
    if "ceiling" in p:
        for ob in bpy.data.collections['GEO'].objects:
            if "_06" in ob.name:
                ob.location[2] = panel_dictionary[p]
print(count)