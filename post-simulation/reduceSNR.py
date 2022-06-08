import os
import json

def return_Y(num, proj):

    me = os.getcwd()
    my_archive = os.path.join(me, "ARCHIVE")
    my_proj = os.path.join(my_archive, proj)
    my_stats = os.path.join(my_proj, "STATS")


    room0 = ["A0_0", "A1_1", "A0_1", "A1_0"]
    room1 = ["A2_2", "A3_3", "A2_3", "A3_2"]
    room2 = ["A4_4", "A5_5", "A4_5", "A5_4"]
    room3 = ["A6_6", "A7_7", "A6_7", "A7_6"]
    room4 = ["A8_8", "A9_9", "A8_9", "A9_8"]
    room5 = ["B0_10", "B1_11", "B0_11", "B1_10"]
    room6 = ["B2_12", "B3_13", "B2_13", "B3_12"]
    room7 = ["B4_14", "B5_15", "B4_15", "B5_14"]

    rooms = [
        room0,
        room1,
        room2,
        room3,
        room4,
        room5,
        room6,
        room7
    ]

    Y = []
    for group in range(num):
        for i, room in enumerate(rooms):
            directs = []
            masks = []

            target_file_name = f"group_{group}_{room[0]}.json"
            with open(os.path.join(my_stats, target_file_name)) as f:
                data = json.load(f)
                directs.append(data['SPL']['data'][8])

            target_file_name = f"group_{group}_{room[1]}.json"
            with open(os.path.join(my_stats, target_file_name)) as f:
                data = json.load(f)
                directs.append(data['SPL']['data'][8])

            target_file_name = f"group_{group}_{room[2]}.json"
            with open(os.path.join(my_stats, target_file_name)) as f:
                data = json.load(f)
                masks.append(data['SPL']['data'][8])

            target_file_name = f"group_{group}_{room[3]}.json"
            with open(os.path.join(my_stats, target_file_name)) as f:
                data = json.load(f)
                masks.append(data['SPL']['data'][8])

            snr_0 = directs[0] - masks[0]
            snr_1 = directs[1] - masks[1]

            snr_avg = round( (snr_0+snr_1) / 2 , 2)

            Y.append(snr_avg)
    return Y