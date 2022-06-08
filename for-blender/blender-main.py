bl_info = {
    "name": "CATT Exporter",
    "author": "OScar Jones",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "View3D",
    "description": "Exports Scene as CATT .GEO, and .LOC files",
    "category": "3D View",
}

import bpy
from bpy.types import Operator, Panel, PropertyGroup
import os
import csv
import numpy as np
import random
import json


### ALL PARAMTERS ###

repeats = 1
number_of_rooms =  8
number_of_panels = 75
height_range = [4,4.4,4.8,5.2,5.6,6.0]
my_path = "C:/Users/otjon/Documents/Imperial/Masters/Project/DREAMFACTORY"



### OPTIONS ###

implementing = False
exporting_floorstanding = False
exporting_panels = False
exporting_zones = False



queue = [i*20 for i in range(number_of_rooms)]

panels_zone_1 = ['absorber_panel_set_01', 'absorber_panel_set_01.001', 'absorber_panel_set_01.005', 'absorber_panel_set_01.006', 'absorber_panel_set_01.010', 'absorber_panel_set_01.011', 'absorber_panel_set_01.015', 'absorber_panel_set_01.016']
panels_zone_2 = ['absorber_panel_set_01.020', 'absorber_panel_set_01.021', 'absorber_panel_set_01.025', 'absorber_panel_set_01.026', 'absorber_panel_set_01.030', 'absorber_panel_set_01.031', 'absorber_panel_set_01.035', 'absorber_panel_set_01.036', 'absorber_panel_set_01.040', 'absorber_panel_set_01.041']
panels_zone_3 = ['absorber_panel_set_01.045', 'absorber_panel_set_01.046', 'absorber_panel_set_01.050', 'absorber_panel_set_01.051', 'absorber_panel_set_01.055', 'absorber_panel_set_01.056', 'absorber_panel_set_01.060', 'absorber_panel_set_01.061']
panels_zone_4 = ['absorber_panel_set_01.002', 'absorber_panel_set_01.003', 'absorber_panel_set_01.004', 'absorber_panel_set_01.007', 'absorber_panel_set_01.008', 'absorber_panel_set_01.009', 'absorber_panel_set_01.012', 'absorber_panel_set_01.013', 'absorber_panel_set_01.014', 'absorber_panel_set_01.017', 'absorber_panel_set_01.018', 'absorber_panel_set_01.019']
panels_zone_5 = ['absorber_panel_set_01.022', 'absorber_panel_set_01.023', 'absorber_panel_set_01.024', 'absorber_panel_set_01.027', 'absorber_panel_set_01.028', 'absorber_panel_set_01.029', 'absorber_panel_set_01.032', 'absorber_panel_set_01.033', 'absorber_panel_set_01.034', 'absorber_panel_set_01.037', 'absorber_panel_set_01.038', 'absorber_panel_set_01.039', 'absorber_panel_set_01.042', 'absorber_panel_set_01.043', 'absorber_panel_set_01.044']
panels_zone_6 = ['absorber_panel_set_01.047', 'absorber_panel_set_01.048', 'absorber_panel_set_01.049', 'absorber_panel_set_01.052', 'absorber_panel_set_01.053', 'absorber_panel_set_01.054', 'absorber_panel_set_01.057', 'absorber_panel_set_01.058', 'absorber_panel_set_01.059', 'absorber_panel_set_01.062', 'absorber_panel_set_01.063', 'absorber_panel_set_01.064']

panels_zone_7 = ['absorber_panel_set_05', 'absorber_panel_set_05.001', 'absorber_panel_set_05.002', 'absorber_panel_set_05.003', 'absorber_panel_set_05.016', 'absorber_panel_set_05.017', 'absorber_panel_set_05.018', 'absorber_panel_set_05.019']
panels_zone_8 = ['absorber_panel_set_05.004', 'absorber_panel_set_05.005', 'absorber_panel_set_05.006', 'absorber_panel_set_05.007', 'absorber_panel_set_05.020', 'absorber_panel_set_05.021', 'absorber_panel_set_05.022', 'absorber_panel_set_05.023']
panels_zone_9 = ['absorber_panel_set_05.008', 'absorber_panel_set_05.009', 'absorber_panel_set_05.010', 'absorber_panel_set_05.011', 'absorber_panel_set_05.024', 'absorber_panel_set_05.025', 'absorber_panel_set_05.026', 'absorber_panel_set_05.027']
panels_zone_10 = ['absorber_panel_set_05.012', 'absorber_panel_set_05.013', 'absorber_panel_set_05.014', 'absorber_panel_set_05.015', 'absorber_panel_set_05.028', 'absorber_panel_set_05.029', 'absorber_panel_set_05.030', 'absorber_panel_set_05.031']
panels_zone_11 = ['absorber_panel_set_05.032', 'absorber_panel_set_05.033', 'absorber_panel_set_05.034', 'absorber_panel_set_05.035', 'absorber_panel_set_05.048', 'absorber_panel_set_05.049', 'absorber_panel_set_05.050', 'absorber_panel_set_05.051', 'absorber_panel_set_05.064', 'absorber_panel_set_05.065', 'absorber_panel_set_05.066', 'absorber_panel_set_05.067']
panels_zone_12 = ['absorber_panel_set_05.036', 'absorber_panel_set_05.037', 'absorber_panel_set_05.038', 'absorber_panel_set_05.039', 'absorber_panel_set_05.052', 'absorber_panel_set_05.053', 'absorber_panel_set_05.054', 'absorber_panel_set_05.055', 'absorber_panel_set_05.068', 'absorber_panel_set_05.069', 'absorber_panel_set_05.070', 'absorber_panel_set_05.071']
panels_zone_13 = ['absorber_panel_set_05.040', 'absorber_panel_set_05.041', 'absorber_panel_set_05.042', 'absorber_panel_set_05.043', 'absorber_panel_set_05.056', 'absorber_panel_set_05.057', 'absorber_panel_set_05.058', 'absorber_panel_set_05.059', 'absorber_panel_set_05.072', 'absorber_panel_set_05.073', 'absorber_panel_set_05.074', 'absorber_panel_set_05.075']
panels_zone_14 = ['absorber_panel_set_05.044', 'absorber_panel_set_05.045', 'absorber_panel_set_05.046', 'absorber_panel_set_05.047', 'absorber_panel_set_05.060', 'absorber_panel_set_05.061', 'absorber_panel_set_05.062', 'absorber_panel_set_05.063', 'absorber_panel_set_05.076', 'absorber_panel_set_05.077', 'absorber_panel_set_05.078', 'absorber_panel_set_05.079']

panels_zone_15 = ['absorber_panel_set_02.012', 'absorber_panel_set_02.013', 'absorber_panel_set_02.014', 'absorber_panel_set_02.015', 'absorber_panel_set_02.028', 'absorber_panel_set_02.029', 'absorber_panel_set_02.030', 'absorber_panel_set_02.031']
panels_zone_16 = ['absorber_panel_set_02.008', 'absorber_panel_set_02.009', 'absorber_panel_set_02.010', 'absorber_panel_set_02.011', 'absorber_panel_set_02.024', 'absorber_panel_set_02.025', 'absorber_panel_set_02.026', 'absorber_panel_set_02.027']
panels_zone_17 = ['absorber_panel_set_02.004', 'absorber_panel_set_02.005', 'absorber_panel_set_02.006', 'absorber_panel_set_02.007', 'absorber_panel_set_02.020', 'absorber_panel_set_02.021', 'absorber_panel_set_02.022', 'absorber_panel_set_02.023']
panels_zone_18 = ['absorber_panel_set_02', 'absorber_panel_set_02.001', 'absorber_panel_set_02.002', 'absorber_panel_set_02.003', 'absorber_panel_set_02.016', 'absorber_panel_set_02.017', 'absorber_panel_set_02.018', 'absorber_panel_set_02.019']
panels_zone_19 = ['absorber_panel_set_02.044', 'absorber_panel_set_02.045', 'absorber_panel_set_02.046', 'absorber_panel_set_02.047', 'absorber_panel_set_02.060', 'absorber_panel_set_02.061', 'absorber_panel_set_02.062', 'absorber_panel_set_02.063', 'absorber_panel_set_02.076', 'absorber_panel_set_02.077', 'absorber_panel_set_02.078', 'absorber_panel_set_02.079']
panels_zone_20 = ['absorber_panel_set_02.040', 'absorber_panel_set_02.041', 'absorber_panel_set_02.042', 'absorber_panel_set_02.043', 'absorber_panel_set_02.056', 'absorber_panel_set_02.057', 'absorber_panel_set_02.058', 'absorber_panel_set_02.059', 'absorber_panel_set_02.072', 'absorber_panel_set_02.073', 'absorber_panel_set_02.074', 'absorber_panel_set_02.075']
panels_zone_21 = ['absorber_panel_set_02.036', 'absorber_panel_set_02.037', 'absorber_panel_set_02.038', 'absorber_panel_set_02.039', 'absorber_panel_set_02.052', 'absorber_panel_set_02.053', 'absorber_panel_set_02.055', 'absorber_panel_set_02.068', 'absorber_panel_set_02.069', 'absorber_panel_set_02.070', 'absorber_panel_set_02.071', 'absorber_panel_set_02.054']
panels_zone_22 = ['absorber_panel_set_02.032', 'absorber_panel_set_02.033', 'absorber_panel_set_02.034', 'absorber_panel_set_02.035', 'absorber_panel_set_02.048', 'absorber_panel_set_02.049', 'absorber_panel_set_02.050', 'absorber_panel_set_02.051', 'absorber_panel_set_02.064', 'absorber_panel_set_02.065', 'absorber_panel_set_02.066', 'absorber_panel_set_02.067']

panels_zone_23 = ['absorber_panel_set_04.004', 'absorber_panel_set_04.005', 'absorber_panel_set_04.006', 'absorber_panel_set_04.007', 'absorber_panel_set_04.012', 'absorber_panel_set_04.013', 'absorber_panel_set_04.014', 'absorber_panel_set_04.015']
panels_zone_24 = ['absorber_panel_set_04', 'absorber_panel_set_04.001', 'absorber_panel_set_04.002', 'absorber_panel_set_04.003', 'absorber_panel_set_04.008', 'absorber_panel_set_04.009', 'absorber_panel_set_04.010', 'absorber_panel_set_04.011']
panels_zone_25 = ['absorber_panel_set_04.020', 'absorber_panel_set_04.021', 'absorber_panel_set_04.022', 'absorber_panel_set_04.023', 'absorber_panel_set_04.028', 'absorber_panel_set_04.029', 'absorber_panel_set_04.030', 'absorber_panel_set_04.031', 'absorber_panel_set_04.036', 'absorber_panel_set_04.037', 'absorber_panel_set_04.038', 'absorber_panel_set_04.039']
panels_zone_26 = ['absorber_panel_set_04.016', 'absorber_panel_set_04.017', 'absorber_panel_set_04.018', 'absorber_panel_set_04.019', 'absorber_panel_set_04.024', 'absorber_panel_set_04.025', 'absorber_panel_set_04.026', 'absorber_panel_set_04.027', 'absorber_panel_set_04.032', 'absorber_panel_set_04.033', 'absorber_panel_set_04.034', 'absorber_panel_set_04.035']

panels_zone_27 = ['absorber_panel_set_03', 'absorber_panel_set_03.001', 'absorber_panel_set_03.002', 'absorber_panel_set_03.003', 'absorber_panel_set_03.004', 'absorber_panel_set_03.005', 'absorber_panel_set_03.006', 'absorber_panel_set_03.007']
panels_zone_28 = ['absorber_panel_set_03.008', 'absorber_panel_set_03.009', 'absorber_panel_set_03.010', 'absorber_panel_set_03.011', 'absorber_panel_set_03.012', 'absorber_panel_set_03.013', 'absorber_panel_set_03.014', 'absorber_panel_set_03.015', 'absorber_panel_set_03.016', 'absorber_panel_set_03.017', 'absorber_panel_set_03.018', 'absorber_panel_set_03.019']

panels_zone_29 = ['absorber_panel_set_06', 'absorber_panel_set_06.001', 'absorber_panel_set_06.002', 'absorber_panel_set_06.003', 'absorber_panel_set_06.013', 'absorber_panel_set_06.014', 'absorber_panel_set_06.015', 'absorber_panel_set_06.016']
panels_zone_30 = ['absorber_panel_set_06.004', 'absorber_panel_set_06.005', 'absorber_panel_set_06.006', 'absorber_panel_set_06.007', 'absorber_panel_set_06.008', 'absorber_panel_set_06.017', 'absorber_panel_set_06.018', 'absorber_panel_set_06.019', 'absorber_panel_set_06.020', 'absorber_panel_set_06.021']
panels_zone_31 = ['absorber_panel_set_06.009', 'absorber_panel_set_06.010', 'absorber_panel_set_06.011', 'absorber_panel_set_06.012', 'absorber_panel_set_06.022', 'absorber_panel_set_06.023', 'absorber_panel_set_06.024', 'absorber_panel_set_06.025']
panels_zone_32 = ['absorber_panel_set_06.026', 'absorber_panel_set_06.027', 'absorber_panel_set_06.028', 'absorber_panel_set_06.029', 'absorber_panel_set_06.039', 'absorber_panel_set_06.040', 'absorber_panel_set_06.041', 'absorber_panel_set_06.042']
panels_zone_33 = ['absorber_panel_set_06.030', 'absorber_panel_set_06.031', 'absorber_panel_set_06.032', 'absorber_panel_set_06.033', 'absorber_panel_set_06.034', 'absorber_panel_set_06.043', 'absorber_panel_set_06.044', 'absorber_panel_set_06.045', 'absorber_panel_set_06.046', 'absorber_panel_set_06.047']
panels_zone_34 = ['absorber_panel_set_06.035', 'absorber_panel_set_06.036', 'absorber_panel_set_06.037', 'absorber_panel_set_06.038', 'absorber_panel_set_06.048', 'absorber_panel_set_06.049', 'absorber_panel_set_06.050', 'absorber_panel_set_06.051']
panels_zone_35 = ['absorber_panel_set_06.052', 'absorber_panel_set_06.053', 'absorber_panel_set_06.054', 'absorber_panel_set_06.055', 'absorber_panel_set_06.065', 'absorber_panel_set_06.066', 'absorber_panel_set_06.067', 'absorber_panel_set_06.068']
panels_zone_36 = ['absorber_panel_set_06.056', 'absorber_panel_set_06.057', 'absorber_panel_set_06.058', 'absorber_panel_set_06.059', 'absorber_panel_set_06.060', 'absorber_panel_set_06.069', 'absorber_panel_set_06.070', 'absorber_panel_set_06.071', 'absorber_panel_set_06.072', 'absorber_panel_set_06.073']
panels_zone_37 = ['absorber_panel_set_06.061', 'absorber_panel_set_06.062', 'absorber_panel_set_06.063', 'absorber_panel_set_06.064', 'absorber_panel_set_06.074', 'absorber_panel_set_06.075', 'absorber_panel_set_06.076', 'absorber_panel_set_06.077']
panels_zone_38 = ['absorber_panel_set_06.078', 'absorber_panel_set_06.079', 'absorber_panel_set_06.080', 'absorber_panel_set_06.081', 'absorber_panel_set_06.091', 'absorber_panel_set_06.092', 'absorber_panel_set_06.093', 'absorber_panel_set_06.094']
panels_zone_39 = ['absorber_panel_set_06.082', 'absorber_panel_set_06.083', 'absorber_panel_set_06.084', 'absorber_panel_set_06.085', 'absorber_panel_set_06.086', 'absorber_panel_set_06.095', 'absorber_panel_set_06.096', 'absorber_panel_set_06.097', 'absorber_panel_set_06.098', 'absorber_panel_set_06.099']
panels_zone_40 = ['absorber_panel_set_06.087', 'absorber_panel_set_06.088', 'absorber_panel_set_06.089', 'absorber_panel_set_06.090', 'absorber_panel_set_06.100', 'absorber_panel_set_06.101', 'absorber_panel_set_06.102', 'absorber_panel_set_06.103']
panels_zone_41 = ['absorber_panel_set_06.104', 'absorber_panel_set_06.105', 'absorber_panel_set_06.106', 'absorber_panel_set_06.107']
panels_zone_42 = ['absorber_panel_set_06.108', 'absorber_panel_set_06.109', 'absorber_panel_set_06.110', 'absorber_panel_set_06.111']

panel_zones = [

panels_zone_1,
panels_zone_2,
panels_zone_3,
panels_zone_4,
panels_zone_5,
panels_zone_6,
panels_zone_7,
panels_zone_8,
panels_zone_9,
panels_zone_10,
panels_zone_11,
panels_zone_12,
panels_zone_13,
panels_zone_14,
panels_zone_15,
panels_zone_16,
panels_zone_17,
panels_zone_18,
panels_zone_19,
panels_zone_20,
panels_zone_21,
panels_zone_22,
panels_zone_23,
panels_zone_24,
panels_zone_25,
panels_zone_26,
panels_zone_27,
panels_zone_28,
panels_zone_29,
panels_zone_30,
panels_zone_31,
panels_zone_32,
panels_zone_33,
panels_zone_34,
panels_zone_35,
panels_zone_36,
panels_zone_37,
panels_zone_38,
panels_zone_39,
panels_zone_40,
panels_zone_41,
panels_zone_42

]
    
global_index = {}
global_index["p"] = 0

if implementing:
    implementation_path = os.path.join(my_path, "IMPLEMENTATION")
    imp_dict = {}

    for i, file in enumerate(os.listdir(implementation_path)):
        print(file)
        imp_dict[i] = file
    

def shuffle_panels_all(height_range, number_of_panels):
    
    f_stand_1 = (0,0)
    f_stand_2 = (0,0)
    
    for panel in bpy.data.collections["GEO"].objects:
        if "absorber" in panel.name:
                panel.hide_viewport = True
                
    for obj in bpy.data.collections["GEO"].objects:
        if "Baffle" in obj.name:
            bpy.data.collections["GEO"].objects[obj.name].hide_viewport = True


    if implementing:
        there_a_baffle = False
        with open(os.path.join(implementation_path, imp_dict[global_index['p']])) as f:
            panel_dictionary = json.load(f)
            count = 0
            for p in panel_dictionary:
                if "absorber" in p:
                    if panel_dictionary[p] == True:
                        count+=1
                    bpy.data.collections["GEO"].objects[p].hide_viewport = not panel_dictionary[p]
                if "Baffle" in p:
                    if panel_dictionary[p][0] > 0:
                        bpy.data.collections["GEO"].objects[p].hide_viewport = False
                        bpy.data.collections["GEO"].objects[p].modifiers["Array"].count = panel_dictionary[p][0]
                        bpy.data.collections["GEO"].objects[p].modifiers["Array"].relative_offset_displace[1] = panel_dictionary[p][1]
                        count += panel_dictionary[p][0]
                        if "001" in p:
                            print("YAS")
                            f_stand_1 = (panel_dictionary[p][0], panel_dictionary[p][1])
                        elif "002" in p:
                            f_stand_2 = (panel_dictionary[p][0], panel_dictionary[p][1])
                        there_a_baffle = True
                if "ceiling" in p:
                    for ob in bpy.data.collections['GEO'].objects:
                        if "_06" in ob.name:
                            ob.location[2] = panel_dictionary[p]
                            new_height = panel_dictionary[p]
        print(count)
    

    if exporting_floorstanding:
        there_a_baffle = True
        standings_1 = [
        (10,-1.1), (9,-1.2), (8,-1.4), (7,-1.6), (6,-1.9),
        (8,-1.1), (7,-1.2), (6,-1.4), (5,-1.6), (4,-1.9),
        (6,-1.1), (5,-1.2), (4,-1.4), (3,-1.6), (2,-1.9),
        (4,-1.1), (3,-1.2), (2,-1.4), (1,-1.6),
        ]

        #standings_1 = [(1,1.5)]

        option = random.choice(standings_1)
        f_stand_1 = option
        c = option[0]
        o = option[1]
        bpy.data.collections["GEO"].objects["Baffles.001"].modifiers["Array"].count = c
        bpy.data.collections["GEO"].objects["Baffles.001"].modifiers["Array"].relative_offset_displace[1] = o

        standings_2 = [
        (6,1.1), (5,1.4), (4,1.9),
        (4,1.1), (3,1.4),
        (2,1.1), (1,1.4)
        ]

        #standings_2 = [(1,1.5)]

        option = random.choice(standings_2)
        f_stand_2 = option
        c = option[0]
        o = option[1]
        bpy.data.collections["GEO"].objects["Baffles.002"].modifiers["Array"].count = c
        bpy.data.collections["GEO"].objects["Baffles.002"].modifiers["Array"].relative_offset_displace[1] = o


    if there_a_baffle:

        ### CREATE DUPLICATES FLOOR BAFFLES AND HIDE ORIGINAL
        for i in ["001","002"]:
            bpy.ops.object.select_all(action='DESELECT')
            for obj in bpy.data.collections['GEO'].objects:
                if f"Baffles.{i}" in obj.name:
                    obj.select_set(True)
            for obj in bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = obj
            bpy.ops.object.duplicate(linked=False)
            bpy.context.view_layer.objects.active.name = f"fuck.{i}"
            bpy.ops.object.select_all(action='DESELECT')
            for obj in bpy.data.collections['GEO'].objects:
                if f"Baffles.{i}" in obj.name:
                    obj.hide_viewport = True

        ### MAKE DUPLICATES REAL
        for i in ["001","002"]:
            bpy.ops.object.select_all(action='DESELECT')  
            for obj in bpy.data.collections['GEO'].objects:
                if f"fuck.{i}" in obj.name:
                    obj.select_set(True)
            for obj in bpy.context.selected_objects:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply(modifier='Array')
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)



    num_floor_standings = f_stand_1[0] + f_stand_2[0]
    num_floor_standings = 0

    panel_dict = {}
    new_height = random.choice(height_range)
    candidate_list = [panel.name for panel in bpy.data.collections["GEO"].objects]



    if implementing:
        with open(os.path.join(implementation_path, imp_dict[global_index['p']])) as f:
            data = json.load(f)
            for zone in panel_zones:
                for panel in zone:
                    bpy.data.collections["GEO"].objects[panel].hide_viewport = not data[panel]


         
    if exporting_panels:
        panel_quota = 0
        target_wall_ceiling = number_of_panels-num_floor_standings

        while panel_quota < target_wall_ceiling:
            candidate = random.choice(candidate_list)
            if "absorber" in candidate:
                if bpy.data.collections["GEO"].objects[candidate].hide_viewport == True:
                    bpy.data.collections["GEO"].objects[candidate].hide_viewport = False
                    panel_quota += 1
                else:
                    pass
            else:
                pass



    if exporting_zones:
        print(global_index["p"])
        if global_index["p"] < 42:
            for panel in panel_zones[global_index["p"]]:
                print(panel)
                bpy.data.collections["GEO"].objects[panel].hide_viewport = False
        else:
            pass


    for panel in bpy.data.collections["GEO"].objects:
        if "absorber" in panel.name:
            if "_06" in panel.name:
                panel.location[2] = new_height
                print(new_height)
    
                
    global_index["p"] += 1
    return f_stand_1, f_stand_2, new_height



def restore_panels():
    ### DELETE DUPLICATES
    for i in ["001","002"]:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.collections['GEO'].objects:
            if f"fuck.{i}" in obj.name:
                bpy.data.objects.remove(bpy.data.objects[f"fuck.{i}"], do_unlink=True)

    ### SHOW ORIGINALS       
    for i in ["001","002"]:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.collections['GEO'].objects:
            if f"Baffles.{i}" in obj.name:
                obj.hide_viewport = False
                
def panel_coverage():               
    panels_tally = dict.fromkeys([i for i in range(42)])
    for key in panels_tally:
        panels_tally[key] = 0
    for i, zone in enumerate(panel_zones):
        for panel in zone:
            if bpy.data.collections["GEO"].objects[panel].hide_viewport == False:
                panels_tally[i] +=1
            else:
                pass
    fracs = []
    totals = []
    for i, zone in enumerate(panel_zones):
        totals.append(panels_tally[i])
        fracs.append(int(panels_tally[i]/len(zone)*100))
    return totals, fracs
                
def export_panel_data(room_counter, total_panels, fracs_panels, height, floor_standings, file_index):
    
    ### SPATIAL ###
    with open(os.path.join(os.path.join(bpy.context.scene.catt_props.export_loc, "DS"), f"room_spat_{file_index}_{room_counter}.csv"), 'w', encoding='UTF8', newline='') as f:
                
        csv_header = ['Name', 'X', 'Y', 'Z']
        csv_data = []

        for item in bpy.data.collections["GEO"].objects:
            if "absorber" in item.name:
                if item.hide_viewport == False:
                    name = item.name
                    l_x,l_y,l_z = item.location[0], item.location[1], item.location[2]
                    csv_data.append([name, l_x, l_y, l_z])
  
        
        floor_stander_origin = [bpy.data.collections["GEO"].objects["Baffles.001"].location[i] for i in range(3)]
        for stander in range(floor_standings[0][0]):
            new_line = [f"Baffles.001.{stander}", floor_stander_origin[0], floor_stander_origin[1]+stander*floor_standings[0][1]*0.6, floor_stander_origin[2]]
            csv_data.append(new_line)
            
        floor_stander_origin = [bpy.data.collections["GEO"].objects["Baffles.002"].location[i] for i in range(3)]
        for stander in range(floor_standings[1][0]):
            new_line = [f"Baffles.002.{stander}", floor_stander_origin[0]+stander*floor_standings[1][1]*0.6, floor_stander_origin[1], floor_stander_origin[2]]
            csv_data.append(new_line)
          
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(csv_data)

    ### BINARY ###
    with open(os.path.join(os.path.join(bpy.context.scene.catt_props.export_loc, "DS"), f"room_bin_{file_index}_{room_counter}.csv"), 'w', encoding='UTF8', newline='') as f:

        csv_header = ['Name', 'State']
        csv_data = []

        for panel in bpy.data.collections["GEO"].objects:
            if "absorber" in panel.name:
                csv_data.append([panel.name, str(not panel.hide_viewport)])
                
        heights = [4,4.4,4.8,5.2,5.6,6.0]
        heights_dict = dict.fromkeys(heights)
        
        for height_band in heights:
            if height == height_band:
                heights_dict[height_band] = True
            else:
                heights_dict[height_band] = False
        
        for height_band in heights:
            csv_data.append([height_band, heights_dict[height_band]])
        
        
        standings_1 = [
        (10,-1.1), (9,-1.2), (8,-1.4), (7,-1.6), (6,-1.9),
        (8,-1.1), (7,-1.2), (6,-1.4), (5,-1.6), (4,-1.9),
        (6,-1.1), (5,-1.2), (4,-1.4), (3,-1.6), (2,-1.9),
        (4,-1.1), (3,-1.2), (2,-1.4), (1,-1.6),
        ]
        
        standings_2 = [
        (6,1.1), (5,1.4), (4,1.9),
        (4,1.1), (3,1.4),
        (2,1.1), (1,1.4)
        ]
        
        for stander_group in standings_1:
            if floor_standings[0] == stander_group:
                csv_data.append([stander_group, True])
            else:
                csv_data.append([stander_group, False])
                
        for stander_group in standings_2:
            if floor_standings[1] == stander_group:
                csv_data.append([stander_group, True])
            else:
                csv_data.append([stander_group, False])
        
        
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(csv_data)

    ### ZONE FRACTIONS ###
    with open(os.path.join(os.path.join(bpy.context.scene.catt_props.export_loc, "DS"), f"room_frac_{file_index}_{room_counter}.csv"), 'w', encoding='UTF8', newline='') as f:
        
        csv_header = ['abs', 'frac']
        csv_data = []
        
        for i in range(len(total_panels)):
            csv_data.append([total_panels[i], fracs_panels[i]])
            
        csv_data.append([height, height])
        
        
        standing_group_1_num = floor_standings[0][0]
        standing_group_2_num = floor_standings[1][0]
        standing_group_1_spa = floor_standings[0][1]
        standing_group_2_spa = floor_standings[1][1]
        
        csv_data.append([standing_group_1_num, int(standing_group_1_num/10*100)])
        csv_data.append([standing_group_2_num, int(standing_group_2_num/6*100)])
        csv_data.append([standing_group_1_spa, abs(int(standing_group_1_spa/1.9*100))])
        csv_data.append([standing_group_2_spa, abs(int(standing_group_2_spa/1.9*100))])
        
        
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(csv_data)

sources_list = [

"A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", 
"B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", 
"C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", 
"D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", 
"E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", 
"F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", 
"G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", 
"H0", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", 
"I0", "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", 
"J0", "J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8", "J9", 
"K0", "K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9", 
"L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", 
"M0", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", 
"N0", "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", 
"O0", "O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8", "O9", 
"P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", 
"Q0", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", 
"R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", 
"S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", 
"T0", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", 
"U0", "U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8", "U9", 
"V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9"

]

class Master():
    def __init__(self):
        
        self.index = 0
        self.healthy = True 
        self.outpath = bpy.context.scene.catt_props.export_loc
        self.directpath = bpy.context.scene.catt_props.direct_loc
        self.assetspath = bpy.context.scene.catt_props.asset_loc
        self.vert_dict = {}
        self.mat_dict = {}
        self.planes_idx = 0
        self.header = ""
        self.planes = ""
        
        try:
            with open (os.path.join(self.assetspath, "CATTmaterials.txt")) as file:
                for line in file:
                    self.header += line
                    material = line.split(" ")[1]
                    self.mat_dict[material] = material
        except FileNotFoundError:
            bpy.context.scene.catt_props.status_deets = "Assets folder not found"
            self.healthy = False
            
        try:
            with open(os.path.join(self.directpath, "test.txt"), 'w') as file:
                file.write("test")
        except FileNotFoundError or PermissionError:
            bpy.context.scene.catt_props.status_deets = "Failed to access Directivities path"
            self.healthy = False  
              
        try:
            with open(os.path.join(self.outpath, "MASTER.GEO"), 'w') as file:
                file.write(";init")
        except FileNotFoundError:
            bpy.context.scene.catt_props.status_deets = "Failed to access Export path"
            self.healthy = False            
            
    def cycle(self, number_of_panels):
        room_counter = 0
        for i in queue:
        
            f_stand_1, f_stand_2, new_height = shuffle_panels_all(height_range, number_of_panels)
            total_panels, fracs_panels = panel_coverage()
            
            export_panel_data(room_counter, total_panels, fracs_panels, new_height, (f_stand_1, f_stand_2), self.index)
            
            for item in bpy.data.collections["GEO"].objects:
                if item.hide_viewport == False:
                    for p in item.data.polygons:
                        vert_idx = []
                        for v in p.vertices:
                            
                            set_vert = [item.data.vertices[v].co[0], item.data.vertices[v].co[1], item.data.vertices[v].co[2], 1]
                            tx = np.array(bpy.data.collections["GEO"].objects[item.name].matrix_world)
                            
                            place_new = np.matmul(tx,set_vert)
                            place_new = place_new
                            
                            x = place_new[0]+i
                            y = place_new[1]
                            z = place_new[2]
                            
                            vert_str = "X {} Y {} Z {}".format(x, y, z)
                            
                            if vert_str not in self.vert_dict:
                                self.vert_dict[vert_str] = len(self.vert_dict) + 1
                            vert_idx.append(self.vert_dict[vert_str])
                        try:
                            plane_material = self.mat_dict[item.material_slots[p.material_index].name]
                            self.add_plane("wall", vert_idx, plane_material)
                        except:
                            bpy.context.scene.catt_props.status_deets = f"Material not in CATTMaterials.txt"
                            self.healthy = False
                            break
                else:
                    pass
                    
            restore_panels()
            room_counter+=1

    def add_plane(self, name, verts, matt):
        self.planes_idx += 1
        vert_string = ""
        for v in verts:
            vert_string += f"{v} "
        out_str = f"[{self.planes_idx} {name} / {vert_string}/ {matt} ]"
        self.planes += f"{out_str} \n"
        
    def list_verts(self):
        dump = ""
        for vert, i in self.vert_dict.items():
            decomp = vert.split(" ")
            x = decomp[1]
            y = decomp[3]
            z = decomp[5]
            export = f"{i} {x} {y} {z}"
            dump += f"{export}\n"
        return dump
        
    def export(self):
        #filename = imp_dict[global_index['p']-1]
        #filename = filename.split(".")[0]
        print(self.index)
        with open (os.path.join(self.outpath, f"MASTER_{self.index}.GEO"), 'w') as file:
            file.write(self.header)
            file.write("\n")
            file.write("\nCORNERS\n")
            file.write(self.list_verts())
            file.write("\nPLANES\n")
            file.write(self.planes)
            
    def export_rec(self):
        with open (os.path.join(self.outpath, f"REC{self.index}.LOC"), 'w') as file:
            file.write("RECEIVERS\n")
            
            count = 0
            
            for idx in queue:
                for i, rec in enumerate(bpy.data.collections['REC'].objects):
                    if rec.hide_viewport == False:
                        X = rec.location[0]+float(idx)
                        Y = rec.location[1]
                        Z = rec.location[2]
                        file.write(f"{count} {X} {Y} {Z}")
                        file.write("\n")
                        count += 1
            
    def export_src(self):
        with open (os.path.join(self.outpath, f"SRC{self.index}.LOC"), 'w') as file:
            
            count = 0
            
            for perm_idx in queue:
                for i, src in enumerate(bpy.data.collections['SRC'].objects):
                    if src.hide_viewport == False:
                        X = src.location[0]+float(perm_idx)
                        Y = src.location[1]
                        Z = src.location[2]
                        idx = int(src.name.split("_")[1])

                        try:
                            tar = bpy.data.collections['TAR'].objects[f"T_{idx}"]
                            X_d = tar.location[0]+float(perm_idx)
                            Y_d = tar.location[1]
                            Z_d = tar.location[2]
                        except KeyError:
                            X_d = 0
                            Y_d = 0
                            Z_d = 0
                            bpy.context.scene.catt_props.status_deets = f"Source has no target: {src.name}"
                            self.healthy = False
                            break
                        try:
                            direct = src.name.split("_")[2]
                        except IndexError:
                            bpy.context.scene.catt_props.status_deets = f"Source has no specified directivity: {src.name}"
                            self.healthy = False
                            break
                        
                        if os.path.isfile(os.path.join(self.directpath, direct)):

                            file.write(f'SOURCE {sources_list[count]}')
                            file.write("\n")
                            file.write(f' DIRECTIVITY = "{direct}"')
                            file.write("\n")
                            file.write(f' POS = {X} {Y} {Z}')
                            file.write("\n")
                            file.write(f' AIMPOS = {X_d} {Y_d} {Z_d}')
                            file.write("\n")
                            file.write(' Lp1m_a = Lp_voice_normal')
                            file.write("\n")
                            file.write(' END')
                            file.write("\n")
                            
                        else:
                            bpy.context.scene.catt_props.status_deets = "Source has no valid directivity"
                            self.healthy = False
                            break
                        count+=1
            file.write('RETURN')

class MoreUtils():
    def __init__(self):
        self.name = "yes"
        self.outpath = bpy.context.scene.catt_props.export_loc
        
    def build_instructions(self, item):
        
        belonging_dict = {}
        count  =0
        room_count = 0
            
        for queued in queue:
            
            for room in bpy.data.collections['BOUNDS'].objects:
                entry = room.name + "_" + str(room_count)
                belonging_dict[entry] = []
                
            for i, rec in enumerate(bpy.data.collections[item].objects):
                if rec.hide_viewport == False:
                    r_x = rec.location[0]
                    r_y = rec.location[1]
                    r_z = rec.location[2]
                    
                    for i, bounds in enumerate(bpy.data.collections['BOUNDS'].objects):
                        bounding_name = bounds.name + "_" + str(room_count)
                        b_x1 = bounds.delta_location[0] - bounds.delta_scale[0]
                        b_x2 = bounds.delta_location[0] + bounds.delta_scale[0]
                        b_y1 = bounds.delta_location[1] - bounds.delta_scale[1]
                        b_y2 = bounds.delta_location[1] + bounds.delta_scale[1]                
                        b_z1 = bounds.delta_location[2] - bounds.delta_scale[2]
                        b_z2 = bounds.delta_location[2] + bounds.delta_scale[2]
                        if b_x1 < r_x < b_x2 and b_y1 < r_y < b_y2 and b_z1 < r_z < b_z2:
                            if item == "SRC":
                                if rec.scale[0] > 1:
                                    belonging_dict[bounding_name].insert(0,"")
                                    belonging_dict[bounding_name].insert(0, sources_list[count])
                                else:
                                    belonging_dict[bounding_name].append(sources_list[count])

                            elif item == "REC":
                                belonging_dict[bounding_name].append(count)
                            else:
                                pass
                        count+=1
                else:
                    pass
            
            room_count+=1
        return belonging_dict

    def export_instructions(self, dict_src, dict_rec):
        ins_dir = os.path.join(self.outpath, "INS")
        if os.path.exists(ins_dir):
            pass
        else:
            os.mkdir(ins_dir)
            
        for room in dict_rec:
            with open (os.path.join(ins_dir, f"{room}.txt"), 'w') as file:
                elements = dict_src[room]
                if len(elements)>2:
                    recorder = 0
                    for e in elements:
                        if len(e)>0:
                            file.write(f"{e}_{dict_rec[room][recorder]}")
                            file.write("\n")
                        else:
                            file.write("\n")
                        recorder+=1
                else:
                    recorder = 0
                    for e in elements:
                        if len(e)>0:
                            file.write(f"{e}_{dict_rec[room][recorder]}")
                            file.write("\n")
                        else:
                            file.write("\n")
                        recorder+=1
                    file.write("None")
    
##############
# ADDON CODE #
##############

class OBJECT_OT_run(Operator):
    bl_idname = "object.run"
    bl_label = "Run CATT Exporter"

    def execute(self, context):
        
        for i in range(repeats):
            # for iteratively increasing number of panels for initial testing
            # number_of_panels = 25 * (i+1)
        
            bpy.context.scene.catt_props.status = ""
            worker = Master()
            worker.index = i
            if worker.healthy:
                worker.cycle(number_of_panels)
                if worker.healthy:
                    worker.export()
                    worker.export_rec()
                    worker.export_src()
                    if worker.healthy:
                        bpy.context.scene.catt_props.status = "CATT files exported"
                        bpy.context.scene.catt_props.status_deets = ""
                    else:
                        bpy.context.scene.catt_props.status = "ERROR: Export interupted"
                else:
                    bpy.context.scene.catt_props.status = "ERROR: Export failed"
            else:
                bpy.context.scene.catt_props.status = "ERROR: Initialisation failed"
                
            
        return {'FINISHED'}

class OBJECT_OT_ins(Operator):
    bl_idname = "object.ins"
    bl_label = "Run Instructions exporter"

    def execute(self, context):
        worker = MoreUtils()
        source_dict = worker.build_instructions("SRC")
        rec_dict = worker.build_instructions("REC")
        worker.export_instructions(source_dict, rec_dict)
        return {'FINISHED'}

class CATTProps(PropertyGroup):
    export_loc: bpy.props.StringProperty(name="Export", subtype='FILE_PATH', default="")
    direct_loc: bpy.props.StringProperty(name="Directivities", subtype='FILE_PATH', default="")
    asset_loc: bpy.props.StringProperty(name="Assets", subtype='FILE_PATH', default="")
    status: bpy.props.StringProperty(name="Status", default="")
    status_deets: bpy.props.StringProperty(name="Status Details", default="")
    
class Panel(Panel):
    bl_label = "Exporter"
    bl_idname = "SCENE_PT_exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CATT'

    def draw(self, context):
        catt_props = bpy.context.scene.catt_props
        layout = self.layout
        layout.label(text="File Paths")
        
        row_loc_export = layout.row()
        row_loc_export.prop(catt_props, "export_loc")
        
        row_loc_direct = layout.row()
        row_loc_direct.prop(catt_props, "direct_loc")
        
        row_loc_asset = layout.row()
        row_loc_asset.prop(catt_props, "asset_loc")
        
        row_export = layout.row()
        row_export.operator("object.run", text="Export")
        
        row_ins = layout.row()
        row_ins.operator("object.ins", text="Build Instructions")
        
        row_status = layout.row()
        row_status.label(text=f"{bpy.context.scene.catt_props.status}")
        
        row_status_deets = layout.row()
        row_status_deets.label(text=f"{bpy.context.scene.catt_props.status_deets}")

classes = [
OBJECT_OT_run,
OBJECT_OT_ins,
CATTProps,
Panel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.catt_props = bpy.props.PointerProperty(type=CATTProps)
    bpy.context.scene.catt_props.status = ""
    bpy.context.scene.catt_props.status_deets = ""
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.catt_props
if __name__ == "__main__":
    register()