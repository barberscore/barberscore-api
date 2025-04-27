def bankers(num):
    """
    Rounds the number based on specific fractional ranges:
      - [0.00, 0.06]: round down to the integer.
      - [0.06, 0.15]: set fractional part to 0.1.
      - [0.15, 0.25]: set fractional part to 0.2.
      - [0.26, 0.35]: set fractional part to 0.3.
      - [0.35, 0.45]: set fractional part to 0.4.
      - [0.45, 0.55]: set fractional part to 0.5.
      - [0.55, 0.65]: set fractional part to 0.6.
      - [0.65, 0.75]: set fractional part to 0.7.
      - [0.75, 0.85]: set fractional part to 0.8.
      - [0.85, 0.95]: set fractional part to 0.9.
      - [0.95, 1.00): round up to the next integer.
      - Otherwise, return the number unchanged.
    """
    if num:
        # Separate integer and fractional parts.
        integer_part = int(num)
        frac = round(num - integer_part, 2)
        
        # Define the intervals and their target fractional values.
        intervals = [
            ((0.00, 0.05), 0.0),
            ((0.05, 0.14), 0.1),
            ((0.14, 0.25), 0.2),
            ((0.26, 0.34), 0.3),
            ((0.34, 0.45), 0.4),
            ((0.45, 0.54), 0.5),
            ((0.54, 0.65), 0.6),
            ((0.65, 0.74), 0.7),
            ((0.74, 0.85), 0.8),
            ((0.85, 0.94), 0.9),
        ]
        
        # Loop through the intervals to check where the fractional part fits.
        for (low, high), target in intervals:
            if low <= frac <= high:
                return integer_part + target
        
        # If the fractional part is in the round-up interval [0.95, 1.00)
        if 0.95 <= frac < 1.00:
            return float(integer_part + 1)

        # If no conditions met, return the original number.
        return num
    else:
        return ""
    
def standard(num):
    """
    Rounds the number based on the following conditions:
      - If the fractional part is between 0.00 and 0.04 (inclusive), round down to the nearest whole number.
      - If the fractional part is between 0.05 and 0.14 (inclusive), set the fractional part to 0.1.
      - If the fractional part is between 0.15 and 0.24 (inclusive), set the fractional part to 0.2.
      - If the fractional part is between 0.25 and 0.34 (inclusive), set the fractional part to 0.3.
      - If the fractional part is between 0.35 and 0.44 (inclusive), set the fractional part to 0.4.
      - If the fractional part is between 0.45 and 0.54 (inclusive), set the fractional part to 0.5.
      - If the fractional part is between 0.55 and 0.64 (inclusive), set the fractional part to 0.6.
      - If the fractional part is between 0.65 and 0.74 (inclusive), set the fractional part to 0.7.
      - If the fractional part is between 0.75 and 0.84 (inclusive), set the fractional part to 0.8.
      - If the fractional part is between 0.85 and 0.94 (inclusive), set the fractional part to 0.9.
      - If the fractional part is between 0.95 and 0.99 (inclusive), round up to the next whole number.
      - Otherwise, return the number unchanged.

    Args:
        num (float): The input number.

    Returns:
        float: The rounded number.
    """
    if num:
        integer_part = int(num)
        fractional_part = round(num - integer_part, 2)

        # List of tuples: (upper_threshold, corresponding fractional value)
        thresholds = [
            (0.04, 0.0),
            (0.14, 0.1),
            (0.24, 0.2),
            (0.34, 0.3),
            (0.44, 0.4),
            (0.54, 0.5),
            (0.64, 0.6),
            (0.74, 0.7),
            (0.84, 0.8),
            (0.94, 0.9)
        ]
        
        for upper, frac in thresholds:
            if fractional_part <= upper:
                return integer_part + frac

        if fractional_part <= 0.99:
            return float(integer_part + 1)
        
        return num
    else:
        return ""

