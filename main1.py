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
  run()

@micropython.native
def run():

    client = simple.MQTTClient(USERNAME, SERVER, user=USERNAME, password=PASSWORD)
    try:
        client.connect()
    except OSError as e:
        restart()

    d = dht.DHT11(machine.Pin(32))
    #machine.freq(80000000)

    try:
        while True:
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
            print("Publish completed")
            print("time: " + str(time.ticks_ms() - startMillis))
            time.sleep(PUB_TIME_SEC)
    except OSError as e:
        restart()


print("Executing main1.py")
run()