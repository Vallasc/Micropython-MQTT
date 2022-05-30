import network

WiFi_SSID = "***********"
WiFi_PASS = "***********"

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WiFi_SSID, WiFi_PASS)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
