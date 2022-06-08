import os
import json
from reduceSNR import return_Y
from matplotlib import pyplot as plt

me = os.getcwd()

SNRs = return_Y(2, "MULTI2-VAL")

print(SNRs)

plt.bar([i+1 for i in range(len(SNRs))], SNRs)
plt.xlabel("Room design")
plt.ylabel("Combined mean signal seperation /dB")
plt.savefig(os.path.join(me, "Best results for SNR optimisation"), dpi=300)
plt.show()