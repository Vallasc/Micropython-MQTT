from credentials import USERNAME, PASSWORD, CHANNEL_ID
from umqtt import simple
import machine
import time
import dht

SERVER = "mqtt3.thingspeak.com"
PUB_TIME_SEC = 5
TOPIC = "channels/" + CHANNEL_ID + "/publish"

def restart():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(5)
  machine.reset()

@micropython.native
def run():
    print("Executing main_low_power.py")

    # Lower the clock to save power
    machine.freq(80000000)

    # MQTT client connection
    client = simple.MQTTClient(USERNAME, SERVER, user=USERNAME, password=PASSWORD)

    # Setup DHT sensor
    d = dht.DHT11(machine.Pin(19))

    try:
        # MQTT client connection
        client.connect()

        # Read DHT sensor
        # Fix error that sometimes after a reset doesn't measure
        for x in range(3):
            try: d.measure(); break
            except: pass

        payload = "field1=" + str(d.temperature()) + "&field2=" + str(d.humidity())
        print("\nTemperature: " + str(d.temperature()))
        print("Humidity: " + str(d.humidity()))

        # Publish data to broker
        client.publish(TOPIC, payload)
        print("Publish completed")
        client.disconnect()
        print("Client disconnected")

    except Exception as e:
        print(e)
        restart()

    print("Going into deep-sleep")
    # Put the device to sleep for PUB_TIME_SEC seconds
    machine.deepsleep(PUB_TIME_SEC*1000)