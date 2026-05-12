from core import *
import network
import socket

PORTAL_SSIDS = ["Free_WiFi_Guest", "Hotel_Internet", "Airport_Free", "CyberStick_AP", "OpenNet"]
SPAM_SSIDS = [
    "CYBERSTICK_ACTIVE",
    "FBI_SURVEILLANCE_VAN",
    "Rick_Owens_Store_Free",
    "MATRIX_GLITCH",
    "PENTAGON_GUEST",
    "VOID_NETWORK",
    "ACCESS_DENIED",
    "ROOT_SHELL",
    "Rick_Astley_5G",
    "CONNECTION_LOST"
]

def beacon_spam():
    cls()
    txt("BEACON SPAM", 25, 0)
    hline(0, 10, 128, 1)
    txt("Initializing AP...", 0, 25)
    show()
    
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    
    count = 0
    running = True
    
    cls()
    txt("SPAMMING AIR...", 15, 20)
    txt("OK = STOP", 35, 50)
    show()
    
    try:
        while running:
            for ssid in SPAM_SSIDS:
                ap.config(essid=ssid)
                time.sleep_ms(1000)
                count += 1
                
                if count % 5 == 0:
                    cls()
                    txt("BEACON SPAM", 25, 0)
                    txt(f"SSIDs sent: {count}", 5, 25)
                    txt(f"Now: {ssid[:13]}", 5, 37)
                    txt("OK to Stop", 30, 55)
                    show()
                
                for _ in range(5):
                    if btn_pressed(btn_ok):
                        running = False
                        break
                    time.sleep_ms(10)
                
                if not running:
                    break
                    
    except Exception as e:
        print("Error:", e)
        cls(); txt("Error!", 40, 25); show(); time.sleep_ms(1000)

    ap.active(False)
    cls(); border(); txt("STOPPED", 35, 28); show()
    time.sleep_ms(1500)

def sd_log(filename, text):
    try:
        import uos
        cs_sd = machine.Pin(PIN_SD_CS, machine.Pin.OUT)
        import machine
        sd = machine.SDCard(slot=1, sck=machine.Pin(18),
            mosi=machine.Pin(23), miso=machine.Pin(19), cs=cs_sd)
        uos.mount(sd, '/sd')
        with open('/sd/' + filename, 'a') as f:
            f.write(text + '\n')
        uos.umount('/sd')
        return True
    except: return False

def wifi_scan():
    cls(); txt("Scanning WiFi...", 5, 28); show()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    nets = wlan.scan()
    if not nets:
        cls(); txt("No Networks!", 20, 28); show()
        time.sleep_ms(1500); return
    nets.sort(key=lambda x: x[3], reverse=True)
    idx = 0
    def draw():
        cls()
        txt("WiFi: " + str(len(nets)), 0, 0)
        hline(0, 10, 128, 1)
        for i in range(min(3, len(nets)-idx)):
            n = nets[idx+i]
            name = n[0].decode('utf-8','ignore')[:11]
            rssi = str(n[3])
            ch   = str(n[2])
            txt(name, 0, 12+i*16)
            txt("ch"+ch, 72, 12+i*16)
            txt(rssi, 100, 12+i*16)
            sec = "O" if n[4]==0 else "*"
            txt(sec, 120, 12+i*16)
        txt("OK=Exit <>Move", 0, 56); show()
    draw()
    while True:
        if btn_pressed(btn_ok): return
        if btn_pressed(btn_left): idx = max(0, idx-1); draw()
        if btn_pressed(btn_right): idx = min(len(nets)-1, idx+1); draw()
        time.sleep_ms(50)

def evil_portal():
    cls(); txt("Evil Portal", 20, 0); hline(0,10,128,1)
    txt("Select SSID:", 0, 14)
    sel = 0
    def draw_sel():
        for i,s in enumerate(PORTAL_SSIDS):
            y = 24+i*8
            if i==sel: fill_rect(0,y-1,128,9,1); txt(s[:15],0,y,0)
            else: txt(s[:15],0,y)
        show()
    draw_sel()
    while True:
        if btn_pressed(btn_ok): break
        if btn_pressed(btn_left): sel=(sel-1)%len(PORTAL_SSIDS); cls(); txt("Select SSID:",0,14); draw_sel()
        if btn_pressed(btn_right): sel=(sel+1)%len(PORTAL_SSIDS); cls(); txt("Select SSID:",0,14); draw_sel()
        time.sleep_ms(50)
    ssid = PORTAL_SSIDS[sel]
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password="12345678")
    cls(); border()
    txt("PORTAL ON", 28, 5)
    txt(ssid[:15], 0, 18); txt("Pass: 12345678", 0, 30)
    txt("IP: 192.168.4.1", 0, 42); txt("OK=Stop", 35, 55); show()
    html = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h2>WiFi Auth</h2></body></html>"
    s = socket.socket(); s.bind(('0.0.0.0', 80)); s.listen(3); s.settimeout(0.3)
    while True:
        if btn_pressed(btn_ok): ap.active(False); s.close(); return
        try: conn, addr = s.accept(); conn.recv(512); conn.send(html); conn.close()
        except: pass

def net_scanner():
    cls(); txt("Net Scanner", 20, 0); hline(0,10,128,1)
    txt("Connect to", 0, 20); txt("WiFi first", 0, 32); txt("OK=Skip", 0, 44); show(); time.sleep_ms(1500)
    wlan = network.WLAN(network.STA_IF); wlan.active(True)
    if not wlan.isconnected():
        cls(); txt("No WiFi!", 30, 25); txt("Connect in your", 0, 37); txt("device settings", 0, 49); show(); time.sleep_ms(2000); return
    ip = wlan.ifconfig()[0]
    subnet = '.'.join(ip.split('.')[:3])
    cls(); txt("Scanning net...", 0, 20); txt(subnet+".0/24", 0, 35); show()
    found = []
    for i in range(1, 255):
        target = subnet + '.' + str(i)
        try: s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(0.1); r = s.connect_ex((target, 80)); s.close()
        except: r = -1
        if r == 0: found.append(target)
        if btn_pressed(btn_ok): break
    idx = 0
    def draw_found():
        cls(); txt("Devices: "+str(len(found)), 0, 0); hline(0,10,128,1)
        if not found: txt("Not found", 28, 30); show(); return
        for i in range(min(4,len(found)-idx)): txt(found[idx+i], 0, 12+i*12)
        txt("OK=Back", 35, 56); show()
    draw_found()
    while True:
        if btn_pressed(btn_ok): return
        if btn_pressed(btn_right): idx=min(max(0,len(found)-4),idx+1); draw_found()
        if btn_pressed(btn_left):  idx=max(0,idx-1); draw_found()
        time.sleep_ms(50)

def sd_logger():
    cls(); txt("SD Logger", 28, 0); hline(0,10,128,1); txt("Logging WiFi", 0, 20); txt("to SD card...", 0, 32); show(); time.sleep_ms(500)
    wlan = network.WLAN(network.STA_IF); wlan.active(True); nets = wlan.scan()
    log = "=== CyberStick WiFi Log ===\n"
    for n in nets: log += n[0].decode()+",ch"+str(n[2])+","+str(n[3])+"dBm\n"
    result = sd_log("wifi_log.txt", log)
    cls(); txt("SD Logger", 28, 0); hline(0,10,128,1)
    if result: txt("Saved!", 40, 25); txt(str(len(nets))+" networks", 25, 37)
    else: txt("SD Error!", 28, 25); txt("Check SD card", 15, 37)
    show(); time.sleep_ms(2000); wait_ok()
