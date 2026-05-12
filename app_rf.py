from core import *

def cc_write(addr, val):
    cs_cc.value(0); spi.write(bytes([addr & 0x3F, val])); cs_cc.value(1)

def cc_read(addr):
    cs_cc.value(0); spi.write(bytes([addr | 0x80])); r = spi.read(1); cs_cc.value(1); return r[0]

def cc_strobe(cmd):
    cs_cc.value(0); spi.write(bytes([cmd])); cs_cc.value(1)

def cc_init():
    cs_cc.value(0); spi.write(bytes([0x30])); cs_cc.value(1)
    time.sleep_ms(10)
    cc_write(0x0B, 0x06); cc_write(0x0D, 0x10)
    cc_write(0x0E, 0xA7); cc_write(0x0F, 0x62)
    cc_write(0x11, 0xF8); cc_write(0x3E, 0xFF)
    cc_strobe(0x34)

def cc_rssi():
    raw = cc_read(0xF4)
    return int((raw-256)/2-74) if raw >= 128 else int(raw/2-74)

def rf_analyzer():
    cls(); txt("CC1101 init...", 0, 28); show()
    try: cc_init(); ok = True
    except: ok = False
    hist = [0]*64; ptr = 0
    while True:
        if btn_pressed(btn_ok): return
        if ok:
            try: rssi = cc_rssi()
            except: rssi = -100
            bar = max(0, min(38, rssi + 100))
        else:
            rssi = -99; bar = 0
        hist[ptr % 64] = bar; ptr += 1
        cls()
        txt("433MHz RF", 28, 0)
        hline(0, 10, 128, 1)
        for i in range(64):
            h = hist[(ptr - 64 + i) % 64]
            if h > 0: vline(i*2, 52-h, h)
        hline(0, 53, 128, 1)
        if ok: txt("RSSI: "+str(rssi)+" dBm", 0, 56)
        else:  txt("NO CC1101", 28, 56)
        show()
        time.sleep_ms(80)
