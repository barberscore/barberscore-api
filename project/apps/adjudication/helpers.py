from math import ceil, floor

def round_up(num, places=1):
    return ceil(num * (10**places)) / float(10**places)