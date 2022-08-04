TOLERANCE = 5
ROUND_P = float(10**TOLERANCE)

def fast_round(some_float):
    """
    https://stackoverflow.com/questions/44920655/python-round-too-slow-faster-way-to-reduce-precision
    """
    return int(some_float * ROUND_P + 0.5)/ROUND_P        

def fast_round_point(some_float):
    return int(some_float[0] * ROUND_P + 0.5)/ROUND_P, int(some_float[1] * ROUND_P + 0.5)/ROUND_P        

