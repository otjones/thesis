import os
import json
import csv
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import blenderInfo as Bi
import random
from statistics import mean
from reduceSNR import return_Y

me = os.getcwd()
dir_learn = os.path.join(me, "LEARN")
dir_learn_2 = os.path.join(me, "LEARN2")

def get_T30(filepath):
    with open(filepath) as f:
        data = json.load(f)
        return data["T-30"]["data"][8]

def get_x_data(filepath):
    with open(filepath) as f:
        data = csv.reader(f, delimiter=',')
        data_list = [row[1] for row in data]
        data_list_cut = data_list[1:]
        data_int = [float(i)/100 for i in data_list_cut]
        return data_int

def make_master(dir_learn, limit):
    master_data = {}
    counter = 0

    all_dir_learn = os.listdir(dir_learn)
    random.shuffle(all_dir_learn)

    for d_set in all_dir_learn:
        if d_set in ["0", "1", "2"]:
            d_set_path = os.path.join(dir_learn, d_set)
            x_path = os.path.join(d_set_path, "X")
            y_path = os.path.join(d_set_path, "Y")

            all_x_path = os.listdir(x_path)
            random.shuffle(all_x_path)

            for x_file in all_x_path:
                x_filename = os.fsdecode(x_file)

                if "frac" in x_filename:
                    code = x_filename.split(".")[0]
                    code = code.split("_frac_")[1]
                    x_data = get_x_data(os.path.join(x_path, x_file))
                    for y_file in os.listdir(y_path):
                        y_filename = os.fsdecode(y_file)
                        if f"_{code}" in y_filename:
                            t_30 = get_T30(os.path.join(y_path, y_file))

                            master_data[counter] = (x_data, t_30)
                            
                            counter+=1

                            if counter > limit:
                                break
                        if counter > limit:
                            break
                    if counter > limit:
                        break
                if counter > limit:
                    break
            if counter > limit:
                break
        if counter > limit:
            break               

    return master_data

def extract(full_set):
    X = []
    Y = []
    for index in full_set:
        X.append(full_set[index][0])
        Y.append(full_set[index][1])
    return X,Y

def load_zone_sizes(me, target):
    std = 15
    ratios = []
    with open(os.path.join(me, target)) as f:
        for line in f:
            if line.strip() != "None":
                ratio = std / int(line.strip())
            else:
                ratio = 1
            ratios.append(ratio)
    return ratios

def calc_zone_weights(coefs, zone_sizes, use):
    if use:
        print(zone_sizes)
        print(coefs)
        zone_sizes_np = np.array([zone_sizes])
        weights = coefs / zone_sizes_np
    else:
        ones = np.ones(len(zone_sizes))
        weights = coefs * ones

    return weights

def compare(model, X, Y):
    table = []
    X_pred = []
    for i, row in enumerate(X):
        pred = model.predict(row.reshape(1,-1))
        table.append((Y[i], pred[0]))
        X_pred.append(pred[0])
    return table, X_pred

def sort_predictions(table_of_Y):
    sorted_table = sorted(table_of_Y, key=lambda x: x[1])
    return sorted_table

def plot_scatter(data):
    X = []
    Y = []
    for i in data:
        X.append(i[0])
        Y.append(i[1])
    plt.scatter(X,Y)
    X_lin = [min(X),max(X)]
    Y_lin = [min(Y),max(Y)]
    plt.plot(X_lin, Y_lin)
    plt.xlabel("Simulated T-30 /s")
    plt.ylabel("Predicted T-30 /s")
    plt.savefig(os.path.join(me, "Predicted T-30 against simulated T-30 for 1000 samples"), dpi=300)
    plt.show()

def remove_outliers(data):
    x_array = np.zeros(len(data))
    for i in range(len(data)):
        x_array[i] = data[i][1]
    p = np.percentile(x_array, 99)
    to_remove = []
    for i in range(len(data)):
        if data[i][1] > p:
            to_remove.append(i)
    for idx in to_remove:
        del data[idx]

def make_y_binary(data, threshold):
    binarised = {}
    count = 0
    for d in data:
        if data[d][1] < threshold:
            binarised[d] = (data[d][0], True)
            count+=1
        else:
            binarised[d] = (data[d][0], False)
    print(f"{count} True elements")
    return binarised

def create_implementation(weights, budget, print_out=False):

    all_panels = {}
    for zone in Bi.panel_zones:
        for panel in zone:
            all_panels[panel] = False

    weights = np.delete(weights, 42, 1)
    sorted = np.argsort(weights)
    priority = [p for p in sorted[0]]
    # if the coeeficients need reversing
    # priority.reverse()

    filling = True
    while filling == True:
        zone = priority.pop()
        filling, num_panels = try_panel(budget, zone)
        panel_names = get_panel_names(zone, num_panels)
        if print_out == True:
            print(f"Zone {zone+1}, {len(panel_names)} panels")

        for i in range(num_panels):
            all_panels[panel_names[i]] = True

        budget -= num_panels

    return all_panels

def create_implementation_snr(weights, budget, print_out=False):

    all_panels = {}
    for zone in Bi.panel_zones:
        for panel in zone:
            all_panels[panel] = False

    all_panels["Baffles.001"] = [0,0]
    all_panels["Baffles.002"] = [0,0]

    ceiling = weights[0][42]
    print(  ceiling)
    weights = np.delete(weights, 42, 1)
    print(len(weights[0]))
    print(len(all_panels))
    sorted = np.argsort(weights)
    priority = [p for p in sorted[0]]
    # if the coefficients need reversing
    # priority.reverse()

    for p in priority:
        print(p, weights[0][p])

    filling = True
    while filling == True:
        zone = priority.pop()
        print(zone)
        if zone < 42:
            filling, num_panels = try_panel(budget, zone)
            panel_names = get_panel_names(zone, num_panels)
            if print_out == True:
                print(f"Zone {zone+1}, {len(panel_names)} panels")

            for i in range(num_panels):
                all_panels[panel_names[i]] = True

            budget -= num_panels
        else:
            if zone == 42 or zone == 44:
                print("Baffles 1")
                if budget > 10:
                    all_panels["Baffles.001"] = [10,-1.1]
                    budget -= 10
                else:
                    all_panels["Baffles.001"] = [budget,-1.1]
                    budget = 0
                    filling = False
            if zone == 43 or zone == 45:
                print("Baffles 2 num")
                if budget > 6:
                    all_panels["Baffles.002"] = [6, 1.1]
                    budget -= 6
                else:
                    all_panels["Baffles.002"] = [budget, 1.1]
                    budget = 0

    if ceiling > 0:
        all_panels["ceiling"] = 6.0
    else:
        all_panels["ceiling"] = 4.0

    return all_panels

def get_panel_names(zone, num):
    return Bi.panel_zones[zone][:num]


def try_panel(budget, zone):
    z = len(Bi.panel_zones[zone])
    if budget <= z:
        return False, budget
    else:
        return True, z

def export_implementations(dictionary, idx, set_size):
    with open(os.path.join(me, f"panel_implementation_{set_size}_{idx}.json"), "w") as f:
        json.dump(dictionary, f)

def setup_X_std(name, type, num):
    X = []
    X_path = os.path.join(dir_learn_2, "X")
    for i in range(num):
        for j in range(8):
            tar_name = f"{name}_{type}_{i}_{j}.csv"
            x_data_point = get_x_data(os.path.join(X_path, tar_name))
            X.append(x_data_point)
    return(X)



# if running multiple regression on randomised datasets, use for loop
# set_size_test used for storing accuracy scores of different dataset sizes 

# set_size_test = {}
# for set_size in range(25, 200, 25):
#     set_size_test[set_size] = []
#     for i in range(10):



model = "Lin"



### LOAD DATA ###
if model == "Lin":
    print("\nLoading Data")
    master_data = make_master(dir_learn, 10000)
    remove_outliers(master_data)
    X,Y = extract(master_data)

elif model == "Log":
    print("\nLoading Data")
    master_data = make_master(dir_learn, 1000)
    remove_outliers(master_data)
    binarised = make_y_binary(master_data, 0.78)
    X,Y = extract(binarised)

elif model == "Lin_multi":
    Y = return_Y(49, "MULTI2")
    X = setup_X_std("room", "frac", 49)
    print(len(X), len(Y))



### FORMAT AND CHECK DATA ###
X_np = np.array(X)
print(X_np.shape)
Y_np = np.array([Y]).reshape(-1,)
print(Y_np.shape)

X_train, X_test, Y_train, Y_test = train_test_split(X_np, Y_np, test_size=0.30, random_state=random.randint(0,100))



### BUILD MODEL ###
print("\nBuilding Model")

if model == "Lin":
    reg = LinearRegression().fit(X_train, Y_train)
    score = reg.score(X_test, Y_test)
    print(score)

    # set_size_test[set_size].append(score)
elif model == "Log":
    reg = LogisticRegression().fit(X_train, Y_train)
    score = reg.score(X_test, Y_test)
    print(score)
    #set_size_test[set_size].append(score)

elif model == "Lin_multi":
    reg = LinearRegression().fit(X_train, Y_train)
    score = reg.score(X_test, Y_test)
    print(score)



### POST ###
print("\nAnalysis")


if model == "Lin":

    plt.hist(Y_np, 25)
    plt.xlabel("T-30 of simulated room /s")
    plt.ylabel("Number of rooms in T-30 bin")
    plt.arrow(0.76, 80, 0, -40, length_includes_head=True, width=0.001, head_width=0.005, head_length=3, fc='k', ec='k')

    # plt.savefig(os.path.join(me, "1000 samples data set T-30s"), dpi=300)
    plt.show()
    print(max(Y_np))
    print(np.percentile(Y_np, 5))
    zone_sizes = load_zone_sizes(me, "zone_sizes.txt")

    weights = calc_zone_weights(reg.coef_, zone_sizes, True)
    print(weights)

    check_predictions, X_pred = compare(reg, X_np, Y_np)
    ordered_predictions = sort_predictions(check_predictions)

    plt.bar([i for i in range(len(weights[0]))], weights[0])
    # plt.savefig(os.path.join(me, "Lin regression coefficients, from 1000 samples data set"), dpi=300)
    plt.xlabel("Parameter weight")
    plt.ylabel("Impact")
    plt.show()

    plt.bar([i for i in range(len(weights[0]))], np.sort(weights[0]))
    # plt.savefig(os.path.join(me, "Lin regression coefficients sorted, from 1000 samples data set"), dpi=300)
    plt.xlabel("Parameter weight")
    plt.ylabel("Impact")
    plt.show()

    # plot_scatter(ordered_predictions)

    print(weights)

    # panel_implementation = create_implementation(weights, 75)
    # export_implementations(panel_implementation, 1, 1000)

    pass

elif model == "Log":
            
    zone_sizes = load_zone_sizes(me, "zone_sizes.txt")
    weights = calc_zone_weights(reg.coef_, zone_sizes, True)
    print(weights)

    check_predictions, X_pred = compare(reg, X_np, Y_np)
    ordered_predictions = sort_predictions(check_predictions)

    plt.bar([i for i in range(len(weights[0]))], weights[0])
    plt.savefig(os.path.join(me, "Log regression coefficients, from 1000 samples data set"), dpi=300)
    plt.xlabel("Parameter weight")
    plt.ylabel("Impact")
    plt.show()

    plt.bar([i for i in range(len(weights[0]))], np.sort(weights[0]))
    plt.savefig(os.path.join(me, "Log regression coefficients sorted, from 1000 samples data set"), dpi=300)
    plt.xlabel("Parameter weight")
    plt.ylabel("Impact")
    plt.show()

    # panel_implementation = create_implementation(weights, 75)
    # export_implementations(panel_implementation, 1, 200)
    
    pass

elif model == "Lin_multi":

    plt.hist(Y_np)
    plt.xlabel("Predicted dB seperation")
    plt.ylabel("Number of observations")
    plt.arrow(7.99, 30, 0, -25, length_includes_head=True, width=0.01, head_width=0.05, head_length=3, fc='k', ec='k')

    # plt.savefig(os.path.join(me, "SNR test predicted histogram with best from model arrow"), dpi=300)
    plt.show()

    check_predictions, X_pred = compare(reg, X_np, Y_np)
    ordered_predictions = sort_predictions(check_predictions)
    # plot_scatter(ordered_predictions)
    print(max(Y_np))

    zone_sizes = load_zone_sizes(me, "zone_sizes_multi.txt")
    weights = calc_zone_weights(reg.coef_, zone_sizes, True)
    print(weights)

    plt.bar([i for i in range(len(weights[0]))], weights[0])
    plt.xlabel("Weighted coefficient")
    plt.ylabel("Impact")
    # plt.savefig(os.path.join(me, "SNR test coefficients"), dpi=300)
    plt.show()

    # panel_implementation = create_implementation_snr(weights, 75)
    # export_implementations(panel_implementation, i, set_size)



# used for analysing multi test results

# converg_data = []
# labels = []
# means = []
# for set_i in set_size_test:
#     converg_data.append(set_size_test[set_i])
#     labels.append(set_i)
#     means.append(mean(set_size_test[set_i]))


# plt.plot(labels, means)
# plt.ylabel("Model score (R squared)")
# plt.xlabel("Size of dataset (70% train 30% test)")

# plt.boxplot(converg_data, labels=labels)
# plt.ylabel("Model score (R squared)")
# plt.xlabel("Size of dataset (70% train 30% test)")

# plt.savefig(os.path.join(me, "chart-1"), dpi=300)
# plt.show()

