import os
import json
from matplotlib import pyplot as plt
import blenderInfo as Bi
import numpy as np

me = os.getcwd()
me_archive = os.path.join(me, "ARCHIVE")
proj = os.path.join(me_archive, "PANEL-ZONES-DET-TEST")
results = os.path.join(proj, "STATS")
ins = os.path.join(proj, "INS")

def load_results():

    X = []
    counter = 0
    for file in os.listdir(results):
        filename = os.fsdecode(file)
        with open(os.path.join(results, file)) as f:
            data = json.load(f)
            t_30 = (3.3 - data["T-30"]["data"][8]) / len(Bi.panel_zones[counter])
            X.append(t_30)
        counter+=1
    X_np = np.array([X])
    print(X_np)
    plt.bar([i for i in range(len(X))], X)
    plt.xlabel("Panel Zone")
    plt.ylabel("Reduction in T-30 /s")
    # plt.savefig(os.path.join(me, "Deterministic method panel importance rankings"), dpi=300)
    plt.show()
    return X_np

def create_implementation(weights):

    all_panels = {}
    for zone in Bi.panel_zones:
        for panel in zone:
            all_panels[panel] = False

    sorted = np.argsort(weights)
    priority = [p for p in sorted[0]]
    # priority.reverse()
    budget = 75

    filling = True
    while filling == True:
        zone = priority.pop()
        filling, num_panels = try_panel(budget, zone)
        panel_names = get_panel_names(zone, num_panels)
        print(f"Zone {zone+1}, {len(panel_names)} panels")

        for i in range(num_panels):
            all_panels[panel_names[i]] = True

        budget -= num_panels

    return all_panels

def get_panel_names(zone, num):
    return Bi.panel_zones[zone][:num]


def try_panel(budget, zone):
    z = len(Bi.panel_zones[zone])
    if budget <= z:
        return False, budget
    else:
        return True, z

def export_implementations(dictionary):
    with open(os.path.join(me, "panel_implementation_det.json"), "w") as f:
        json.dump(dictionary, f)

weights = load_results()

#panel_implementation = create_implementation(weights)
#export_implementations(panel_implementation)