from matplotlib import pyplot as plt
import os

me = os.getcwd()

no_panels = 3.39
lorenzo = 1.53
seperable = 1.08
pimp = 0.76

names = ["None", "Convention", "Seperation", "Regression"]
X = [no_panels, lorenzo, seperable, pimp]
colours = ["Black", "Black", "Black", "Blue"]

plt.bar(names, X, color=colours)
plt.xlabel("Optimisation method")
plt.ylabel("T-30 measure /s")
plt.savefig(os.path.join(me, "Optimisation methods compared"), dpi=300)
plt.show()
