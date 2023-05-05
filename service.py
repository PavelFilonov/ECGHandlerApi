import json
import math
import os

import neurokit2 as nk
from pyedflib import highlevel

import repository


def detect_and_save_edf(file, first_name, last_name, gender, age, date_start):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'file.edf')
    with open(file_path, 'wb') as f:
        f.write(file.read())

    patient_id = repository.save_patient(first_name, last_name, gender, age)

    signals, signal_headers, header = highlevel.read_edf(file_path)
    for i in range(len(signal_headers)):
        signal = signals[i]
        signal_header = signal_headers[i]

        lead = signal_header['label'].lstrip('ECG ').rstrip('-Ref')
        sample_rate = signal_header['sample_rate']
        period = 1 / sample_rate

        file_id = repository.save_file(convert_signal_to_json(signal, period), lead, period, date_start, patient_id)

        _, r_peaks = nk.ecg_peaks(signal, sampling_rate=sample_rate)
        _, waves_peak = nk.ecg_delineate(signal, r_peaks, sampling_rate=sample_rate, method="peak")

        p_peaks = waves_peak['ECG_P_Peaks']
        q_peaks = waves_peak['ECG_Q_Peaks']
        s_peaks = waves_peak['ECG_S_Peaks']
        t_peaks = waves_peak['ECG_T_Peaks']

        repository.save_peaks(convert_peak_time_value(delete_nan(p_peaks), period), file_id, "P")
        repository.save_peaks(convert_peak_time_value(delete_nan(q_peaks), period), file_id, "Q")
        repository.save_peaks(convert_peak_time_value(delete_nan(r_peaks['ECG_R_Peaks']), period), file_id, "R")
        repository.save_peaks(convert_peak_time_value(delete_nan(s_peaks), period), file_id, "S")
        repository.save_peaks(convert_peak_time_value(delete_nan(t_peaks), period), file_id, "T")


def convert_signal_to_json(signal, period):
    points = []
    for i in range(len(signal)):
        points.append({'x': period * i, 'y': signal[i], 'order': i})
    return json.dumps(points)


def delete_nan(lst):
    return [item for item in lst if not (math.isnan(item)) is True]


def convert_peak_time_value(lst, period):
    return [round(period * item, 3) for item in lst]
