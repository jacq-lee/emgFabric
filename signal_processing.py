import numpy as np
import matplotlib.pyplot as plt


def clean_data(data_path, stop_time):
    EMG_data = np.loadtxt(data_path, dtype = int)
    data_length = EMG_data.shape[0]
    time_array = np.linspace(0, stop_time, num = data_length)
    sampling_rate = np.reciprocal(np.divide(stop_time, data_length))
    plt.plot(time_array, EMG_data[:, 0])
    plt.show()

trial1_data_path = "./Arduino EMG Data/trial1.txt"
trial1_stop_time = 82.11

clean_data(trial1_data_path, trial1_stop_time)



