import os
import json
from matplotlib import pyplot as plt

me = os.getcwd()

def main(me, source):
    print(me)
    destination = os.path.join(me, "ARCHIVE")
    destination = os.path.join(destination, source)
    destination = os.path.join(destination, "STATS")

    X = []

    for file in os.listdir(destination):
        with open(os.path.join(destination, file)) as f:
            data = json.load(f)
            X.append(data["T-30"]["data"][8])

    plt.hist(X)
    plt.show()

main(me, "PANELS-75-WITH-CARPET-V-CEILING")
