
def step(time, delay):
    """This is a heavyside step function with a delay.
    """
    return float(time>=delay)