from credentials import USERNAME, PASSWORD, CHANNEL_ID
from umqtt import simple
import machine
import time
import dht

SERVER = "mqtt3.thingspeak.com"
PUB_TIME_SEC = 5
TOPIC = "channels/" + CHANNEL_ID + "/publish"

# Error handling
def restart():
    print('Failed to send data to MQTT broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

@micropython.native
def run():
    print("Executing main_normal.py")

    # Lower the clock to save power
    machine.freq(80000000)

    # MQTT client connection
    client = simple.MQTTClient(USERNAME, SERVER, user=USERNAME, password=PASSWORD)

    # Setup DHT sensor
    d = dht.DHT11(machine.Pin(19))

    try:
        client.connect()
        while True:
            # Read DHT sensor
            # Fix error that sometimes after a reset doesn't measure
            for _ in range(3):
                try: d.measure(); break
                except: pass

            payload = "field1=" + str(d.temperature()) + "&field2=" + str(d.humidity())
            print("\nTemperature: " + str(d.temperature()))
            print("Humidity: " + str(d.humidity()))

            # Publish data to broker
            client.publish(TOPIC, payload)
            print("Publish completed")

            time.sleep(PUB_TIME_SEC)
    except Exception as e:
        print(e)
        restart()