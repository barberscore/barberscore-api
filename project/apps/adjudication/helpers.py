from math import ceil, floor

def round_up(num, places=1):
    return ceil(num * (10**places)) / float(10**places)

def bankers_round(num, places=1):
    return floor(num * (10**places)) / float(10**places)

def truncate_number(value, n):
    return floor(value * 10 ** n) / 10 ** n