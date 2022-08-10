from matplotlib import pyplot as plt
import pandas as pd
import datetime
import numpy as np
import gzip
import shutil
from tqdm import tqdm
import os
import pickle


def load_pickle(pickle_file):
    try:
        with open(pickle_file, 'rb') as f:
            pickle_data = pickle.load(f)
    except UnicodeDecodeError as e:
        with open(pickle_file, 'rb') as f:
            pickle_data = pickle.load(f, encoding='latin1')
    except Exception as e:
        print('Unable to load data ', pickle_file, ':', e)
        raise
    return pickle_data


# ids = pd.read_csv("./graph_sensor_locations_bay.csv", header=None)
sensor_ids, sensor_id_to_ind, adj_mx = load_pickle("./adj_mx_bay.pkl")

target_sensors = sensor_ids

paths = os.listdir("raw_data")
paths = [os.path.join("raw_data", p) for p in paths]
for path in paths:
    for file0 in (pbar := tqdm(os.listdir(path))):
        with gzip.open(f'{path}/{file0}', 'rb') as f_in:
            with open('temp.txt', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        data = pd.read_table("temp.txt", sep=",", header=None)
        data = data.iloc[:, :12]
        data.columns = ["timestamp", "station", "district", "freeway",
                        "direction", "lanetype", "station_length", "samples", "observed_percentage",
                        "total_flow", "avg_occ", "avg_speed"]
        # filter data by station in station_list
        target_sensors = [int(x) for x in target_sensors]
        data = data[data['station'].isin(target_sensors)]

        out = np.zeros((288, len(target_sensors), 3))

        out[:, :, 2] = np.stack([(np.arange(288) / 288)] * 325, 1)

        none_list = []

        for k, v in sensor_id_to_ind.items():
            f_data = data[data['station'] == int(k)]

            if len(f_data) == 0:
                none_list.append(k)
                continue

            start = datetime.datetime.strptime(f_data.iloc[0]['timestamp'], '%m/%d/%Y %H:%M:%S')

            for t in range(f_data.shape[0]):
                dt = datetime.datetime.strptime(f_data.iloc[t]['timestamp'], '%m/%d/%Y %H:%M:%S')
                delta = dt - start
                delta = delta.total_seconds() / 60
                t0 = int(delta / 5)
                delta = delta / (24 * 60)

                out[t0, v, 0] = f_data.iloc[t]['total_flow']
                out[t0, v, 1] = f_data.iloc[t]['avg_speed']
                out[t0, v, 2] = delta

        np.save(f'processed_data/{"_".join(file0.split(".")[0].split("_")[-3:])}', out)
        pbar.set_description(f"Processing {file0} - NaNs: {none_list}\n")


processed_data = os.listdir('processed_data')
final_out = np.zeros((288*len(processed_data), len(target_sensors), 3))
for i in range(len(processed_data)):
    data = np.load(f'processed_data/{processed_data[i]}')
    final_out[i*288:(i+1)*288, :, :] = data

# plt.plot((final_out[:, :, 1] == 0).sum(1))
# plt.ylim(0, 10)

np.save('PEMSBAY_2022.npy', final_out)
