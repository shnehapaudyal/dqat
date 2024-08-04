
def calculate_timeliness(df, current_date, last_modification_date, creation_date):
    timeliness = (current_date - last_modification_date) / (current_date - creation_date) * 100
    return timeliness
