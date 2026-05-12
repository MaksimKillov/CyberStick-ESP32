import machine
import ssd1306
import time

PIN_OK = 14     
PIN_LEFT = 16
PIN_RIGHT = 15

PIN_IR = 4
PIN_SD_CS = 13

btn_ok    = machine.Pin(PIN_OK,    machine.Pin.IN, machine.Pin.PULL_UP)
btn_left  = machine.Pin(PIN_LEFT,  machine.Pin.IN, machine.Pin.PULL_UP)
btn_right = machine.Pin(PIN_RIGHT, machine.Pin.IN, machine.Pin.PULL_UP)
ir_pin    = machine.Pin(PIN_IR,    machine.Pin.IN)

i2c  = machine.I2C(0, scl=machine.Pin(21), sda=machine.Pin(22))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0,
    sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19))
cs_cc = machine.Pin(5, machine.Pin.OUT)
cs_cc.value(1)

def btn_pressed(pin):
    if pin.value() == 0:
        time.sleep_ms(20)
        if pin.value() == 0:
            while pin.value() == 0:
                time.sleep_ms(10)
            return True
    return False

def wait_ok():
    while not btn_pressed(btn_ok):
        pass

def cls(): oled.fill(0)
def show(): oled.show()
def txt(s, x, y, c=1): oled.text(s, x, y, c)
def border():
    oled.hline(0,0,128,1); oled.hline(0,63,128,1)
    oled.vline(0,0,64,1);  oled.vline(127,0,64,1)
def fill_rect(x,y,w,h,c=1): oled.fill_rect(x,y,w,h,c)
def rect(x,y,w,h,c=1): oled.rect(x,y,w,h,c)
def vline(x,y,h,c=1): oled.vline(x,y,h,c)
def hline(x,y,w,c=1): oled.hline(x,y,w,c)
