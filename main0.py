import dht
from credentials import USERNAME, PASSWORD, CHANNEL_ID
import utils
from umqtt import simple
import time
import machine

SERVER = "mqtt3.thingspeak.com"
PUB_TIME_SEC = 3
TOPIC = "channels/" + CHANNEL_ID + "/publish"

print("Executing main0.py")

client = simple.MQTTClient(USERNAME, SERVER, user=USERNAME, password=PASSWORD)
client.connect()

d = dht.DHT11(machine.Pin(32))

while True:
    startMillis = time.ticks_ms()

    temp_mean = 0
    hum_mean = 0

    for i in range(10):
        utils.measure(d)
        temp_mean += d.temperature()
        hum_mean += d.humidity()

    temp_mean /= 10
    hum_mean /= 10

    payload = "field1=" + str(temp_mean) + "&field2=" + str(hum_mean)
    print("\nTemperature: " + str(temp_mean))
    print("Humidity: " + str(hum_mean))

    client.publish(TOPIC, payload)
    print("Publish completed")

    print("time: " + str(time.ticks_ms() - startMillis))
    time.sleep(PUB_TIME_SEC)