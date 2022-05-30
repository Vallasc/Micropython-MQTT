import time
from machine import *

freq(240000000)



# def performanceTest():
#     millis = time.ticks_ms
#     endTime = millis() + 10000
#     count = 0
#     while millis() < endTime:
#         count += 1
#     print("Count: ", count)

# @micropython.native
# def performanceTestNative():
#     millis = time.ticks_ms
#     endTime = millis() + 10000
#     count = 0
#     while millis() < endTime:
#         count += 1
#     print("Count2: ", count)

# performanceTest()
# performanceTestNative()

# pin = Pin(13, Pin.OUT)

startMillis = time.ticks_ms()
for i in range(1000000):
    pin.on()
    pin.off()  
print(time.ticks_ms() - startMillis)

@micropython.native
def speed():
    p0 = Pin(13, Pin.OUT)
    millis = time.ticks_ms
    startMillis = millis()
    for i in range(1000000):
        p0.on()
        p0.off()  
    print(millis() - startMillis)

speed()