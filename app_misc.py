import bluetooth
from core import *

def ir_receiver():
    cls(); txt("IR Receiver", 20, 0); hline(0,10,128,1); txt("Waiting signal...", 0, 28); txt("OK=Back", 35, 55); show()
    while True:
        if btn_pressed(btn_ok): return
        if ir_pin.value() == 0:
            pulses = []; t = time.ticks_ms()
            while time.ticks_diff(time.ticks_ms(), t) < 150:
                start = time.ticks_us()
                while ir_pin.value() == 0:
                    if time.ticks_diff(time.ticks_us(), start) > 20000: break
                pulses.append(time.ticks_diff(time.ticks_us(), start))
                start = time.ticks_us()
                while ir_pin.value() == 1:
                    if time.ticks_diff(time.ticks_us(), start) > 20000: break
                pulses.append(time.ticks_diff(time.ticks_us(), start))
            if len(pulses) > 8:
                cls(); txt("IR Receiver", 20, 0); hline(0,10,128,1); txt("SIGNAL!", 35, 14)
                txt("Pulses: "+str(len(pulses)), 0, 26); txt("T1: "+str(pulses[0])+" us", 0, 38); show(); time.sleep_ms(2500)
                cls(); txt("IR Receiver",20,0); hline(0,10,128,1); txt("Waiting signal...",0,28); show()
        time.sleep_ms(10)


ble = bluetooth.BLE()

def bt_scan():
    ble.active(True)
    devices = []
    
    def bt_irq(event, data):
        if event == 5:
            addr = ''.join(['%02X' % b for b in data[1]])
            if addr not in [d[0] for d in devices]:
                devices.append((addr, data[3]))
                
    ble.irq(bt_irq)
    ble.gap_scan(5000, 30000, 30000)
    
    t_end = time.time() + 5
    while time.time() < t_end:
        cls(); txt("BT Scanning...", 20, 25); txt(f"Found: {len(devices)}", 20, 37); show()
        if btn_pressed(btn_ok): break
    
    if not devices:
        cls(); txt("No devices", 30, 25); show(); time.sleep(2); return

    idx = 0
    while True:
        cls(); txt("BT DEVICES", 25, 0); hline(0,10,128,1)
        for i in range(min(4, len(devices)-idx)):
            addr, rssi = devices[idx+i]
            txt(f"{addr[:12]}", 2, 12+i*12)
            txt(f"{rssi}dB", 90, 12+i*12)
        show()
        
        if btn_pressed(btn_ok):
            target = devices[idx][0]
            bt_target_spam(target)
            return
        if btn_pressed(btn_left): return
        if btn_pressed(btn_right): idx = (idx + 1) % len(devices)

def bt_target_spam(addr_str):
    cls(); txt("TARGET SPAM", 25, 0); txt(f"Target: {addr_str[:8]}", 0, 20); txt("OK to Stop", 25, 50); show()
    
    ble.active(True)
    adv_data = bytearray([0x02, 0x01, 0x06, 0x03, 0x03, 0xF1, 0xFF, 0x0C, 0x09, 0x43, 0x79, 0x62, 0x65, 0x72, 0x53, 0x74, 0x69, 0x63, 0x6B])
    
    while not btn_pressed(btn_ok):
        ble.gap_advertise(100, adv_data=adv_data)
        time.sleep_ms(100)
    ble.gap_advertise(None)
    
def about():
    cls(); border(); txt("CYBERSTICK", 5, 5); txt("on base ESP32-D0WD-V3", 10, 18); txt("by MAKSIM KILLOV", 18, 30); txt("OK=Back", 35, 55); show(); wait_ok()
