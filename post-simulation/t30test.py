import os
import json
from matplotlib import pyplot as plt
me = os.getcwd()

my_archive = os.path.join(me, "ARCHIVE")

my_proj = os.path.join(my_archive, "CONVERG-LIN")

my_stats = os.path.join(my_proj, "STATS")

X_25 = []
X_50 = []
X_100 = []
X_200 = []
X_500 = []
X_1000 = []

X = [X_25, X_50, X_100, X_200, X_500, X_1000]

labels = [25, 50, 100, 200, 500, 1000]

for file in os.listdir(my_stats):
    file_group = int(file.split("_")[1])
    print(file_group)
    with open(os.path.join(my_stats, file)) as f:
        data = json.load(f)
            
        X[file_group].append(data["T-30"]["data"][8])


plt.boxplot(X, labels=labels)
plt.xlabel("Size of dataset used to build model")
plt.ylabel("T-30 scores from models")
# plt.savefig(os.path.join(me, "Rate of convergence of logistic regression outcomes with 8 random data subsets per batch size"), dpi=300)
plt.show()

print(X_1000)