import os
import shutil

me = os.getcwd()

def make_INS(folder, num):

    body = "A0_0\nA1_1\nA2_2\nA3_3\nA4_4\nA5_5\nA6_6\nA7_7\nNone"
    body = "A0_0\nA1_1\nA0_1\nA1_0\nNone\nA2_2\nA3_3\nA2_3\nA3_2\nNone\nA4_4\nA5_5\nA4_5\nA5_4\nNone\nA6_6\nA7_7\nA6_7\nA7_6\nNone\nA8_8\nA9_9\nA8_9\nA9_8\nNone\nB0_10\nB1_11\nB0_11\nB1_10\nNone\nB2_12\nB3_13\nB2_13\nB3_12\nNone\nB4_14\nB5_15\nB4_15\nB5_14\nNone"

    desination = os.path.join(me, "ARCHIVE")
    desination = os.path.join(desination, folder)
    desination = os.path.join(desination, "INS")

    for i in range(1,num+1):
        with open(os.path.join(desination, f"multi_{i}.txt"), "w") as f:
            f.write(body)


make_INS("MULTI2", 49)