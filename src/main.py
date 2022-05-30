from umqtt import simple
import random
import time
import dht
import machine

USERNAME = "***********"
PASSWORD = "***********"

SERVER = "mqtt3.thingspeak.com"

CHANNEL_ID = "***********"
WRITE_API_KEY = "***********"
PUB_TIME_SEC = 3

topic = "channels/" + CHANNEL_ID + "/publish"


def restart():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(5)
  machine.reset()

def measure(dht):
    for x in range(3):
        try:
            dht.measure()
            return
        except OSError as e:
            pass
    raise Exception("Measure error")

def run():
    client = simple.MQTTClient(USERNAME, SERVER, user=USERNAME, password=PASSWORD)
    try:
        client.connect()
    except OSError as e:
        restart()

    d = dht.DHT11(machine.Pin(32))
    freq = machine.freq

    try:
        while True:
            measure(d)
            payload = "field1=" + str(d.temperature()) + "&field2=" + str(d.humidity())
            print("\nTemperature: " + str(d.temperature()))
            print("Humidity: " + str(d.humidity()))

            client.publish(topic, payload)
            print("Publish completed")
            freq(80000000)
            time.sleep(PUB_TIME_SEC)
            freq(240000000)
    except OSError as e:
        restart()

def run_deepsleep():
    client = simple.MQTTClient(USERNAME, SERVER, user=USERNAME, password=PASSWORD)
    d = dht.DHT11(machine.Pin(32,machine.Pin.IN, machine.Pin.PULL_UP))
    try:
        client.connect()
        measure(d)
        payload = "field1=" + str(d.temperature()) + "&field2=" + str(d.humidity())
        print("\nTemperature: " + str(d.temperature()))
        print("Humidity: " + str(d.humidity()))
        client.publish(topic, payload)
        client.disconnect()
    except Exception:
        restart()

    print("Publish completed")
    print("Going into deep-sleep")
    # put the device to sleep for PUB_TIME_SEC seconds
    machine.deepsleep(PUB_TIME_SEC*1000)

# run()
run_deepsleep()