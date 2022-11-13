import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import signal 


def clean_data(data_path, stop_time):
    EMG_data = np.loadtxt(data_path, dtype = int)
    EMG_data = np.abs(np.diff(EMG_data))
    data_length = EMG_data.size
    time_array = np.linspace(0, stop_time, num = data_length)
    sampling_rate = np.reciprocal(np.divide(stop_time, data_length))
    
    '''
    plt.figure()
    plt.plot(time_array, EMG_data)
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (mV)")
    plt.title("EMG Data")
    plt.show()
    '''

    return EMG_data, time_array, sampling_rate

trial1_data_path = "./Arduino EMG Data/trial1.txt"
trial1_stop_time = 82.11

trial2_data_path = "./Arduino EMG Data/trial2.txt"
trial2_stop_time = 67.61

(EMG_data_1, time_array_1, sampling_rate_1) = clean_data(trial1_data_path, trial1_stop_time)
(EMG_data_2, time_array_2, sampling_rate_2) = clean_data(trial2_data_path, trial2_stop_time)

def filter_data(emg_data, sampling_rate, order):
    nyquist_frequency = sampling_rate/2
    
    # bandpass filter to clean data
    high = 20/500
    low = 450/500
    b, a = sp.signal.butter(order, [high,low], btype='bandpass')

    emg_filtered = sp.signal.filtfilt(b, a, emg_data, axis=0)

    emg_rectified = np.abs(emg_filtered)
    
    # lowpass filter to obtain the envelope
    low_pass = 0.5/nyquist_frequency
    b2, a2 = sp.signal.butter(order, low_pass, btype='lowpass')

    emg_envelope = sp.signal.filtfilt(b2, a2, emg_rectified, axis=0)

    return emg_envelope

emg_data_envelope = filter_data(EMG_data_2, sampling_rate_2, 4)

plt.figure()
plt.plot(time_array_2, emg_data_envelope)
plt.xlabel('Time (s)')
plt.ylabel('EMG Signal')
plt.title('Filtered EMG Data')
plt.show()