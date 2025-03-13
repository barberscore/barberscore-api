from math import ceil, floor
from decimal import Decimal, ROUND_HALF_DOWN

def round_up(num, places=1):
    return ceil(num * (10**places)) / float(10**places)

