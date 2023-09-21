import pandas as pd

def calculate_rate(row):
    lock_date = row['lock-date']
    if pd.isnull(lock_date):  # If lock-date is empty, use the 2006-2022 rates
        return calculate_2006_2022_rate(row)
    elif lock_date >= pd.Timestamp(1998, 1, 1) and lock_date <= pd.Timestamp(1999, 12, 31):
        return calculate_1998_1999_rate(row)
    elif lock_date >= pd.Timestamp(2000, 1, 1) and lock_date <= pd.Timestamp(2001, 12, 31):
        return calculate_2000_2001_rate(row)
    elif lock_date >= pd.Timestamp(2002, 1, 1) and lock_date <= pd.Timestamp(2003, 12, 31):
        return calculate_2002_2003_rate(row)
    elif lock_date >= pd.Timestamp(2004, 1, 1) and lock_date <= pd.Timestamp(2005, 12, 31):
        return calculate_2004_2005_rate(row)
    else:
        return calculate_2006_2022_rate(row)

def calculate_1998_1999_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.071 * (row['rate-percent'] / 100)
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.071 * (row['rate-percent'] / 100)
        else:
            return (row['track-minutes'] + 1) * 0.0135 * (row['rate-percent'] / 100)
    elif row['rate-type'] == 'Min Stat':
        return 0.071 * (row['rate-percent'] / 100)
    else:
        return None  # Handle unknown rate-types if needed

def calculate_2000_2001_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.0755 * (row['rate-percent'] / 100)
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.0755 * (row['rate-percent'] / 100)
        else:
            return (row['track-minutes'] + 1) * 0.0145 * (row['rate-percent'] / 100)
    elif row['rate-type'] == 'Min Stat':
        return 0.0755 * (row['rate-percent'] / 100)
    else:
        return None  # Handle unknown rate-types if needed

def calculate_2002_2003_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.08 * (row['rate-percent'] / 100)
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.08 * (row['rate-percent'] / 100)
        else:
            return (row['track-minutes'] + 1) * 0.0155 * (row['rate-percent'] / 100)
    elif row['rate-type'] == 'Min Stat':
        return 0.08 * (row['rate-percent'] / 100)
    else:
        return None  # Handle unknown rate-types if needed

def calculate_2004_2005_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.085 * (row['rate-percent'] / 100)
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.085 * (row['rate-percent'] / 100)
        else:
            return (row['track-minutes'] + 1) * 0.0165 * (row['rate-percent'] / 100)
    elif row['rate-type'] == 'Min Stat':
        return 0.085 * (row['rate-percent'] / 100)
    else:
        return None  # Handle unknown rate-types if needed

def calculate_2006_2022_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.091 * (row['rate-percent'] / 100)
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.091 * (row['rate-percent'] / 100)
        else:
            return ((row['track-minutes'] + 1) * 0.0175) * (row['rate-percent'] / 100)
    elif row['rate-type'] == 'Min Stat':
        return 0.091 * (row['rate-percent'] / 100)
    else:
        return None  # Handle unknown rate-types if needed
    
def calculate_rate_period(lock_date):
    if lock_date >= pd.Timestamp(1998, 1, 1) and lock_date <= pd.Timestamp(1999, 12, 31):
        return '1998-1999'
    elif lock_date >= pd.Timestamp(2000, 1, 1) and lock_date <= pd.Timestamp(2001, 12, 31):
        return '2000-2001'
    elif lock_date >= pd.Timestamp(2002, 1, 1) and lock_date <= pd.Timestamp(2003, 12, 31):
        return '2002-2003'
    elif lock_date >= pd.Timestamp(2004, 1, 1) and lock_date <= pd.Timestamp(2005, 12, 31):
        return '2004-2005'
    elif lock_date >= pd.Timestamp(2006, 1, 1) and lock_date <= pd.Timestamp(2022, 12, 31):
        return '2006-2022'
    else:
        return None  # No rate-period for empty lock-date or outside specified periods

def calculate_net_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    else:
        return (row['share'] / 100) * row['rate']