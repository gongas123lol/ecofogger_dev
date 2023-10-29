from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import dht
import time


def read_keypad():
    keys = [None, None]
    for i, row in enumerate(rows):
        row.off()
        for j, col in enumerate(cols):
            if not col():
                keys = [i, j]
        row.on()
    return keys

def time2seconds(hh, mm):
    return (hh*60 + mm) * 60

def update_display():
    oled.fill(0)
    oled.text("Temp:", str(temperature), "ºC" 0, 0)
    oled.text("Humidity:", str(humidity),"%", 0, 16)
    
    if setting_mode:
        oled.text("1 - Set Timer", 0, 48)
        oled.text("2 - Set Humidity", 0, 56)
        oled.text("3 - Set Interval", 0, 64)
        oled.text("* To Exit", 0, 72)
    else:
        oled.text("Min Humidity: {}%".format(minimum_humidity), 0, 48)

    if pump_active:
        oled.text("Pump: ON", 80, 48)
    else:
        oled.text("Pump: OFF", 80, 48)

    oled.show()
