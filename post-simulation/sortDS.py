from dataclasses import replace
from fileinput import filename
import os
from posixpath import split
import shutil
import json

me = os.getcwd()

class walle():

    def __init__(self, me, project):
        self.me = os.path.join(os.path.join(me, "ARCHIVE"), project)
        self.ins = os.path.join(self.me, "INS")
        self.stats = os.path.join(self.me, "STATS")
        self.results = os.path.join(self.me, "RESULTS")
        self.stat_dict = {}
        self.batch_dict = {}


    ### create a dictionary of all INS
    def load_ins(self):
        for file in os.listdir(self.ins):
            filename = os.fsdecode(file)
            batch = filename.split(".")[0]
            self.batch_dict[batch] = []

            with open(os.path.join(self.ins, file)) as f:
                for line in f:
                    print(line)
                    if line.strip() != 'None':
                        self.batch_dict[batch].append(line.strip())
        print(self.batch_dict)

    ### create JSON file in STATS directories from raw data
    def create_stats(self):
        for batch in self.batch_dict:
            for pair in self.batch_dict[batch]:
                print(pair)
                src, rec = pair.split("_")[0], pair.split("_")[1].zfill(2)
                pair_to_check = src+"_"+rec
                batch_to_check = batch+"_"
                print(batch, pair_to_check)
                for file in os.listdir(self.results):
                    filename = os.fsdecode(file)
                    if pair_to_check in filename and batch_to_check in filename:
                        print(filename)

                        batch_index = int(batch.split("_")[1])-1

                        with open( os.path.join(self.results, filename)) as f:
                            glob = []
                            for line in f:
                                glob.append(line)
                            parsed = self.stats_parser(glob)
                            json_file = os.path.join(self.stats, f'group_{batch_index}_{pair}.json')
                            with open(json_file, 'w') as outfile:
                                json.dump(parsed, outfile)


    ### takes raw txt data and returns dict for C-80, RT, T-30, SPL
    def stats_parser(self, raw):
        results_dict = {"C-80":{"unit": "", "data": []}, "RT'":{"unit": "", "data": []}, "T-30":{"unit": "", "data": []}, "SPL":{"unit": "", "data": []}}
        interest = ["C-80", "RT'", "T-30", "SPL"]
        for i, line in enumerate(raw):
            if any(key in line for key in interest):
                r_type, r_data, r_unit = self.clean_up(line)
                results_dict[r_type]["data"] = r_data
                results_dict[r_type]["unit"] = r_unit
        return results_dict


    ### takes raw line and returns reading_type, reading_data, reading_unit
    def clean_up(self, line):
        for i in range(5):
            line = line.replace("  ", " ")
            line = line.replace("\t", " ")
        splitted_line = line.split(' ')
        reading_type = splitted_line[0]
        reading_unit = splitted_line[-1]
        reading_data = splitted_line[2:-1]
        for i, point in enumerate(reading_data):
            if point == "---":
                reading_data[i] = 0
            if point == '"---"':
                reading_data[i] = 0
        return reading_type.replace('"', ''), [float(i) for i in reading_data], reading_unit.replace('"', '').strip()


cube = walle(me, "MULTI2-VAL")
cube.load_ins()
cube.create_stats()