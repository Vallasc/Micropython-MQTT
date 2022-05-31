import time
from machine import *

freq(240000000)

# Unptimized code
p0 = Pin(13, Pin.OUT)
m0 = time.ticks_ms()
for i in range(1000000):
    p0.on()
    p0.off()  
print(time.ticks_ms() - m0)

# Optimized code
@micropython.native
def optimized():
    p1 = Pin(13, Pin.OUT)
    millis = time.ticks_ms
    m1 = millis()
    for i in range(1000000):
        p1.on()
        p1.off()  
    print(millis() - m1)

optimized()