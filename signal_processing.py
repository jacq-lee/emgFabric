import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import signal 


def clean_data(data_path, time_path):
    emg_data = np.loadtxt(data_path, dtype=int)
    emg_data = np.abs(np.diff(emg_data))
    data_length = emg_data.size

    contraction_times = np.loadtxt(time_path, dtype=float)
    stop_time = contraction_times[-1]
    time_data = np.linspace(0, stop_time, num = data_length)

    sampling_rate = np.reciprocal(np.divide(stop_time, data_length))
    
    '''
    plt.figure()
    plt.plot(time_array, EMG_data)
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (mV)")
    plt.title("Raw EMG Data")
    plt.show()
    '''

    return emg_data, contraction_times, time_data, sampling_rate

trial2_data_path = "./Arduino EMG Data/trial2.txt"
trial2_time_path = "./Arduino EMG Data/trial2_contraction_times.txt"

emg_data_raw, contraction_time_array, time_array, samp_rate = clean_data(trial2_data_path, trial2_time_path)

def filter_data(emg_data, sampling_rate, order):
    nyquist_frequency = sampling_rate/2

    # Bandpass filter to clean data
    high_cutoff_band = 0.75/nyquist_frequency
    low_cutoff_band = 15/nyquist_frequency
    b_band, a_band = sp.signal.butter(order, [high_cutoff_band,low_cutoff_band], btype='bandpass')

    emg_filtered = sp.signal.filtfilt(b_band, a_band, emg_data, axis=0)

    emg_rectified = np.abs(emg_filtered)
    
    # Lowpass filter to obtain the envelope
    low_cutoff_lowpass = 0.5/nyquist_frequency
    b_low, a_low = sp.signal.butter(order, low_cutoff_lowpass, btype='lowpass')

    emg_envelope = sp.signal.filtfilt(b_low, a_low, emg_rectified, axis=0)

    return emg_envelope

emg_data_envelope = filter_data(emg_data_raw, samp_rate, 4)

plt.figure()
plt.plot(time_array, emg_data_envelope)
plt.xlabel('Time (s)')
plt.ylabel('EMG Signal')
plt.title('Filtered EMG Data')
plt.show()

#hstack with time array