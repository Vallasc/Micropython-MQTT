import time

def measure(dht):
    for x in range(3):
        try:
            dht.measure()
            return
        except OSError as e:
            pass
    raise Exception("Measure error")