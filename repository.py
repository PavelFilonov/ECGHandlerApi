import numpy as np
from psycopg2.extensions import register_adapter, AsIs

from connection import open_db, close_db
from query.insert import *


def save_patient(first_name, last_name, gender, age):
    connection, cursor = open_db()
    cursor.execute(insert_patient, {'first_name': first_name, 'last_name': last_name, 'gender': gender, 'age': age})
    patient_id = cursor.fetchall()[0][0]
    close_db(connection, cursor)
    return patient_id


def save_file(signal, lead, period, date_start, patient_id):
    connection, cursor = open_db()
    cursor.execute(insert_file,
                   {'content': signal, 'patient_id': patient_id, 'lead': lead,
                    'period': period, 'date_start': date_start})
    file_id = cursor.fetchall()[0][0]
    close_db(connection, cursor)
    return file_id


def save_peaks(peaks, file_id, type_peak):
    connection, cursor = open_db()
    for peak in peaks:
        cursor.execute(insert_peak, {'time_value': float(peak), 'file_id': file_id, 'type_peak': type_peak})
    close_db(connection, cursor)
