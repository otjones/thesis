import os
import shutil
from glob import glob
import json
import numpy as np
import matplotlib.pyplot as plt
import colorsys
from scipy.interpolate import interp1d
import math
import statistics as sts

me = os.getcwd()

class axiom():

    def __init__(self, me, projects):
        self.me = {}
        for project in projects:
            self.me[project] = {}
            self.me[project]["ROOT"] = os.path.join(os.path.join(me, "ARCHIVE"), project)
            self.me[project]["INS"] = os.path.join(self.me[project]["ROOT"], "INS")
            self.me[project]["STATS"] = os.path.join(self.me[project]["ROOT"], "STATS")
            self.analysis = os.path.join(me, "ANALYSIS")
            self.me[project]["ROOM_DICT"] = {}
        self.all_T30 = {}


    def load_ins(self):
        for project in self.me:
            for file in os.listdir(self.me[project]["INS"]):
                filename = os.fsdecode(file)
                room = filename.split(".")[0]
                self.me[project]["ROOM_DICT"][room] = []

                with open(os.path.join(self.me[project]["INS"], file)) as f:
                    for line in f:
                        if line != "None":
                            self.me[project]["ROOM_DICT"][room].append(line.strip())


    def define_T30(self, bins):
        for bin in bins:
            self.all_T30[bin] = []


    def load_stats_T30(self, mapping):
        for project in self.me:
            for room in self.me[project]["ROOM_DICT"]:
                for pair in self.me[project]["ROOM_DICT"][room]:
                    file = f"{room}_{pair}.json"
                    with open(os.path.join(self.me[project]["STATS"], file)) as f:
                        data = json.load(f)
                        dest_bin = mapping[room]
                        self.all_T30[dest_bin].append(data["T-30"]["data"])

    
    def plot_T30(self):

        print("\nExporting Panel number comparisons\n")
        data_1 = [ set[8] for set in self.all_T30["25"] ]
        data_2 = [ set[8] for set in self.all_T30["50"] ]
        data_3 = [ set[8] for set in self.all_T30["75"] ]
        data_4 = [ set[8] for set in self.all_T30["100"] ]
        data_5 = [ set[8] for set in self.all_T30["125"] ]
        data_6 = [ set[8] for set in self.all_T30["150"] ]
        data_7 = [ set[8] for set in self.all_T30["175"] ]
        data_8 = [ set[8] for set in self.all_T30["200"] ]

        data = [data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8]
        labels = [name for name in self.all_T30]

        for i, d in enumerate(data):
            print(f"Exporting {labels[i]} panel rooms distribution, n = {len(d)}")
            plt.hist(d)
            plt.ylabel("Number of rooms")
            plt.xlabel("T-30 /s")
            y_axis_list = range(0, int(len(data[0])/2))
            plt.yticks(y_axis_list)
            plt.savefig(os.path.join(self.analysis, f"Distribution of {labels[i]} panel room performances"), dpi=300)
            plt.clf()

        print("Exporting Boxplot Comparison")
        plt.boxplot(data, labels=labels)
        plt.ylabel("T-30 /s")
        plt.xlabel("Number of panels in room")
        plt.savefig(os.path.join(self.analysis, "T-30 (s) for set numbers of acoustic panels, randomly placed in 16 configurations for each quantity"), dpi=300)
        plt.show()

        print("\nFinsihed\n")

    def plot_T30_carp(self):

        print("\nExporting Panel number comparisons (carpeted)\n")
        data_1 = [ set[8] for set in self.all_T30["25"] ]
        data_2 = [ set[8] for set in self.all_T30["50"] ]
        data_3 = [ set[8] for set in self.all_T30["75"] ]
        data_4 = [ set[8] for set in self.all_T30["100"] ]
        data_5 = [ set[8] for set in self.all_T30["125"] ]
        data_6 = [ set[8] for set in self.all_T30["150"] ]
        data_7 = [ set[8] for set in self.all_T30["175"] ]
        data_8 = [ set[8] for set in self.all_T30["200"] ]

        data = [data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8]
        labels = [name for name in self.all_T30]

        for i, d in enumerate(data):
            print(f"Exporting {labels[i]} panel rooms distribution (carpeted), n = {len(d)}")
            plt.hist(d)
            plt.ylabel("Number of rooms")
            plt.xlabel("T-30 /s")
            y_axis_list = range(0, int(len(data[0])/2))
            plt.yticks(y_axis_list)
            plt.savefig(os.path.join(self.analysis, f"Distribution of {labels[i]} panel room performances (carpeted)"), dpi=300)
            plt.clf()

        print("Exporting Boxplot Comparison")
        plt.boxplot(data, labels=labels)
        plt.ylabel("T-30 /s")
        plt.xlabel("Number of panels in room")
        plt.savefig(os.path.join(self.analysis, "T-30 (s) for set numbers of acoustic panels, randomly placed in 16 configurations for each quantity, (carpeted)"), dpi=300)
        plt.show()

        print("\nFinsihed\n")

    def pounds_per_second(self):
        data_1 = [ set[8] for set in self.all_T30["25"] ]
        data_2 = [ set[8] for set in self.all_T30["50"] ]
        data_3 = [ set[8] for set in self.all_T30["75"] ]
        data_4 = [ set[8] for set in self.all_T30["100"] ]
        data_5 = [ set[8] for set in self.all_T30["125"] ]
        data_6 = [ set[8] for set in self.all_T30["150"] ]
        data_7 = [ set[8] for set in self.all_T30["175"] ]
        data_8 = [ set[8] for set in self.all_T30["200"] ]

        data = [data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8]

        panel_num = [25,50,75,100,125,150,175,200]
        median_T30 = []
        cost = []
        improvement = []
        cost_per_improvement = []

        for i, d in enumerate(data):
            m = sts.median(d)
            median_T30.append(m)
            c = panel_num[i] * 99
            cost.append(c)
            imp = 3.3-m
            improvement.append(imp)
            c_p_i = c/imp
            cost_per_improvement.append(c_p_i)

        plt.plot(cost,median_T30)
        plt.xlabel("Cost of panels /£")
        plt.ylabel("Median T-30 time /s")
        plt.savefig(os.path.join(self.analysis, "Cost to achieve median T-30 times"), dpi=300)
        plt.show()

        early_gradient = (cost_per_improvement[1] - cost_per_improvement[0]) / (25)
        c_intercept = cost_per_improvement[0]
        y_straight = [early_gradient*(p-25) + c_intercept for p in panel_num]


        plt.plot(panel_num,cost_per_improvement)
        plt.plot(panel_num, y_straight)
        plt.xlabel("Number of panels")
        plt.ylabel("Cost per T-30 improvement £/s")
        plt.savefig(os.path.join(self.analysis, "Cost to improve median T-30 times"), dpi=300)
        plt.show()

    def pounds_per_second_carp(self, carpet_cost):
        data_1 = [ set[8] for set in self.all_T30["25"] ]
        data_2 = [ set[8] for set in self.all_T30["50"] ]
        data_3 = [ set[8] for set in self.all_T30["75"] ]
        data_4 = [ set[8] for set in self.all_T30["100"] ]
        data_5 = [ set[8] for set in self.all_T30["125"] ]
        data_6 = [ set[8] for set in self.all_T30["150"] ]
        data_7 = [ set[8] for set in self.all_T30["175"] ]
        data_8 = [ set[8] for set in self.all_T30["200"] ]

        data = [data_1, data_2, data_3, data_4, data_5, data_6, data_7, data_8]

        panel_num = [25,50,75,100,125,150,175,200]
        median_T30 = []
        cost = []
        improvement = []
        cost_per_improvement = []

        for i, d in enumerate(data):
            m = sts.median(d)
            median_T30.append(m)
            c = (panel_num[i] * 99) + (carpet_cost*105)
            cost.append(c)
            imp = 3.3-m
            improvement.append(imp)
            c_p_i = c/imp
            cost_per_improvement.append(c_p_i)

        plt.plot(cost,median_T30)
        plt.xlabel("Cost of panels + carpet /£")
        plt.ylabel("Median T-30 time /s")
        plt.savefig(os.path.join(self.analysis, f"Cost to achieve median T-30 times, carpeted (£{carpet_cost})"), dpi=300)
        plt.show()

        early_gradient = (cost_per_improvement[1] - cost_per_improvement[0]) / (25)
        c_intercept = cost_per_improvement[0]
        y_straight = [early_gradient*(p-25) + c_intercept for p in panel_num]


        plt.plot(panel_num,cost_per_improvement)
        plt.plot(panel_num, y_straight)
        plt.xlabel("Number of panels")
        plt.ylabel("Cost per T-30 improvement £/s")
        plt.savefig(os.path.join(self.analysis, f"Cost to improve median T-30 times, carpeted (£{carpet_cost})"), dpi=300)
        plt.show()


def comp_carpet(me, with_carpet, without_carpet, carpet_cost):

    analysis = os.path.join(me, "ANALYSIS")

    print("\nExporting carpet comparisons\n")
    
    with_carpet_1 = [ set[8] for set in with_carpet.all_T30["25"] ]
    with_carpet_2 = [ set[8] for set in with_carpet.all_T30["50"] ]
    with_carpet_3 = [ set[8] for set in with_carpet.all_T30["75"] ]
    with_carpet_4 = [ set[8] for set in with_carpet.all_T30["100"] ]
    with_carpet_5 = [ set[8] for set in with_carpet.all_T30["125"] ]
    with_carpet_6 = [ set[8] for set in with_carpet.all_T30["150"] ]
    with_carpet_7 = [ set[8] for set in with_carpet.all_T30["175"] ]
    with_carpet_8 = [ set[8] for set in with_carpet.all_T30["200"] ]

    without_carpet_1 = [ set[8] for set in without_carpet.all_T30["25"] ]
    without_carpet_2 = [ set[8] for set in without_carpet.all_T30["50"] ]
    without_carpet_3 = [ set[8] for set in without_carpet.all_T30["75"] ]
    without_carpet_4 = [ set[8] for set in without_carpet.all_T30["100"] ]
    without_carpet_5 = [ set[8] for set in without_carpet.all_T30["125"] ]
    without_carpet_6 = [ set[8] for set in without_carpet.all_T30["150"] ]
    without_carpet_7 = [ set[8] for set in without_carpet.all_T30["175"] ]
    without_carpet_8 = [ set[8] for set in without_carpet.all_T30["200"] ]

    data = [without_carpet_1, with_carpet_1, without_carpet_2, with_carpet_2, without_carpet_3, with_carpet_3, without_carpet_4, with_carpet_4, without_carpet_5, with_carpet_5, without_carpet_6, with_carpet_6, without_carpet_7, with_carpet_7, without_carpet_8, with_carpet_8]
    labels = [name for name in without_carpet.all_T30]

    labels_x2 = []

    for lable in labels:
        labels_x2.append(f"{lable}nc")
        labels_x2.append(f"{lable}c")

    print("Exporting Boxplot Comparison")
    plt.boxplot(data, labels=labels_x2)
    plt.ylabel("T-30 /s")
    plt.xlabel("Number of panels in room")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(analysis, "T-30 (s) for set numbers of acoustic panels, randomly placed in 16 configurations for each quantity, comparing with without carpet"), dpi=300)
    plt.show()

    panel_num = [25,25,50,50,75,75,100,100,125,125,150,150,175,175,200,200]
    median_T30_nc = []
    median_T30_c = []
    cost_nc = []
    cost_c = []
    improvement_nc = []
    improvement_c = []
    cost_per_improvement_nc = []
    cost_per_improvement_c = []

    for i, d in enumerate(data):
        if i%2 == 0:
            m = sts.median(d)
            median_T30_nc.append(m)
            c = (panel_num[i] * 99)
            cost_nc.append(c)
            imp = 3.3-m
            improvement_nc.append(imp)
            c_p_i = c/imp
            cost_per_improvement_nc.append(c_p_i)
        else:
            m = sts.median(d)
            median_T30_c.append(m)
            c = (panel_num[i] * 99) + (carpet_cost*105)
            cost_c.append(c)
            imp = 3.3-m
            improvement_c.append(imp)
            c_p_i = c/imp
            cost_per_improvement_c.append(c_p_i)


    plt.plot(cost_nc,median_T30_nc)
    plt.plot(cost_c,median_T30_c)
    plt.xlabel("Cost /£")
    plt.ylabel("Median T-30 time /s")
    plt.savefig(os.path.join(analysis, f"Cost to achieve median T-30 times comparing with without carpet (£{carpet_cost})"), dpi=300)
    plt.show()

    plt.plot(labels,median_T30_nc)
    plt.plot(labels,median_T30_c)
    plt.xlabel("Number of panels")
    plt.ylabel("Median T-30 time /s")
    plt.savefig(os.path.join(analysis, f"Number of panels to achieve median T-30 times comparing with without carpet (£{carpet_cost})"), dpi=300)
    plt.show()








### T-30 JUST PANELS
"""
cap = axiom(me, ["PANEL-NUMBER-COMP-1", "PANEL-NUMBER-COMP-2"])
cap.load_ins()

bins = ["25", "50", "75", "100", "125", "150", "175", "200"]
mapping = {"room0":"25", "room1":"50", "room2":"75", "room3":"100", "room4":"125", "room5":"150", "room6":"175", "room7":"200"}
cap.define_T30(bins)
cap.load_stats_T30(mapping)
cap.plot_T30()
cap.pounds_per_second()
"""


### T-30 PANELS AND CARPET
"""
cap = axiom(me, ["PANEL-NUMBER-COMP-CARP-1", "PANEL-NUMBER-COMP-CARP-2"])
cap.load_ins()

bins = ["25", "50", "75", "100", "125", "150", "175", "200"]
mapping = {"room0":"25", "room1":"50", "room2":"75", "room3":"100", "room4":"125", "room5":"150", "room6":"175", "room7":"200"}
cap.define_T30(bins)
cap.load_stats_T30(mapping)
cap.plot_T30_carp()
cap.pounds_per_second_carp(14)
"""

### COMPARE NO CARPET TO CARPET
"""
bins = ["25", "50", "75", "100", "125", "150", "175", "200"]
mapping = {"room0":"25", "room1":"50", "room2":"75", "room3":"100", "room4":"125", "room5":"150", "room6":"175", "room7":"200"}

no_carpet = axiom(me, ["PANEL-NUMBER-COMP-1", "PANEL-NUMBER-COMP-2"])
no_carpet.load_ins()
no_carpet.define_T30(bins)
no_carpet.load_stats_T30(mapping)

with_carpet = axiom(me, ["PANEL-NUMBER-COMP-CARP-1", "PANEL-NUMBER-COMP-CARP-2"])
with_carpet.load_ins()
with_carpet.define_T30(bins)
with_carpet.load_stats_T30(mapping)

comp_carpet(me, with_carpet, no_carpet, 14)
"""

### CALCULATE NUMBER OF PANELS CARPETD
"""
carpet_cost = 14
total_cost = 6500
panel_num = 75

print(( total_cost - (carpet_cost*105) ) / 99)

print((panel_num * 99) + (carpet_cost*105))
"""