import dht
from credentials import USERNAME, PASSWORD, CHANNEL_ID
import utils
from umqtt import simple
import machine
import time

SERVER = "mqtt3.thingspeak.com"
PUB_TIME_SEC = 3
TOPIC = "channels/" + CHANNEL_ID + "/publish"

def restart():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(5)
  machine.reset()

@micropython.native
def run():
    print("Executing main_low_power.py")
    client = simple.MQTTClient(USERNAME, SERVER, user=USERNAME, password=PASSWORD)
    d = dht.DHT11(machine.Pin(32,machine.Pin.IN, machine.Pin.PULL_UP))
    try:
        client.connect()
        startMillis = time.ticks_ms()
        
        temp_mean = 0
        hum_mean = 0
        for i in range(10):
            utils.measure(d)
            temp_mean += d.temperature()
            hum_mean += d.humidity()
        temp_mean = str(temp_mean/10)
        hum_mean = str(hum_mean/10)

        payload = "field1=" + temp_mean + "&field2=" + hum_mean
        print("\nTemperature: " + temp_mean)
        print("Humidity: " + hum_mean)
        client.publish(TOPIC, payload)
        client.disconnect()
    except Exception:
        restart()

    print("Publish completed")
    print("Going into deep-sleep")
    # put the device to sleep for PUB_TIME_SEC seconds
    machine.deepsleep(PUB_TIME_SEC*1000)