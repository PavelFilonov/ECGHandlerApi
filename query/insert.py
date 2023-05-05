insert_patient = \
    f'''
        insert into patient (first_name, last_name, gender, age)
        values (%(first_name)s, %(last_name)s, %(gender)s, %(age)s)
        returning id;
    '''

insert_file = \
    f'''
        insert into file (content, patient_id, lead, period, date_start)
        values (%(content)s, %(patient_id)s, %(lead)s, %(period)s, %(date_start)s)
        returning id;
    '''

insert_peak = \
    f'''
        insert into peak (time_value, file_id, type_peak)
        values (%(time_value)s, %(file_id)s, %(type_peak)s)
        returning id;
    '''
