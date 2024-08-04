def calculate_volatility(current_date, creation_date, modification_date):
    volatility = (creation_date - modification_date) / (current_date - creation_date) * 100
    return volatility