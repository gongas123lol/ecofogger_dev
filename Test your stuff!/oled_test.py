from machine import Pin,I2C
import ssd1306
from time import sleep
import utime
import machine
import dht
import _thread

WIDTH  = 128                                            
HEIGHT = 64                                             
 
i2c = I2C(0,scl=Pin(1), sda=Pin(0),freq = 400000) #Init i2c
oled=ssd1306.SSD1306_I2C(128,64,i2c,0x3c)
dht_sensor = dht.DHT11(Pin(16))

oled.text_encoding = 'utf-8'

def clear_display():
    oled.fill(0)
    oled.show()

def update_display1():
    
    oled.fill(0)
    oled.text("Hello      ", 0, 0)
    oled.text("this is a test!", 0, 16)

    oled.show()
    

def update_display2():
   
    oled.fill(0)
    oled.text("     World", 0, 0)
    oled.text("this is a test!", 0, 16)

    oled.show()



# MAIN LOOP -------------------------------------------------------------------------------------------

while True:
    update_display1()
    utime.sleep(1)
    update_display2()
    utime.sleep(1)
    
    

