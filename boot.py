import network
import time
import main
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        for _ in range(10):
            if wlan.isconnected(): break
            time.sleep(1)
    print('Network config:', wlan.ifconfig())

connect_wifi('Name', 'Password')
main.splash()
main.main_loop()