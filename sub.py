
def my_round(val, digit=0):
    p = 10 ** digit
    rounded = (val * p * 2 + 1) // 2 / p
    return int(rounded) if digit == 0 else rounded