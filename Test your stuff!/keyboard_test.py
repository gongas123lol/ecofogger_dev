from machine import Pin,I2C
import ssd1306
from time import sleep
import utime
import machine
import dht
import _thread

# Create a map between keypad buttons and characters
matrix_keys = [['1', '2', '3'],
               ['4', '5', '6'],
               ['7', '8', '9'],
               ['*', '0', '#']]

# PINs according to schematic - Change the pins to match with your connections
keypad_rows = [4,5,6,7]
keypad_columns = [8,9,10]

kpress = None

# Create two empty lists to set up pins ( Rows output and columns input )
row_pins = []
col_pins = []

# Loop to assign GPIO pins and setup input and outputs
for x in range(0,4):
    row_pins.append(Pin(keypad_rows[x], Pin.OUT))
    row_pins[x].value(1)
for x in range(0,3):
    col_pins.append(Pin(keypad_columns[x], Pin.IN, Pin.PULL_DOWN))
    col_pins[x].value(0)
    
##############################Scan keys ####################
    
    
def scankeys():
    global key_press
    while True:
        for row in range(4):
            for col in range(3):
                row_pins[row].high()
                if col_pins[col].value() == 1:
                    key_press = matrix_keys[row][col]
                    print("You have pressed:", key_press)
                    utime.sleep(0.3)
                row_pins[row].low()



# Remember the pico had 2 cores? lets use them and free up the main one!

_thread.start_new_thread(scankeys, ())


