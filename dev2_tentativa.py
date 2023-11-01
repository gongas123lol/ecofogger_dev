from machine import Pin,I2C
import ssd1306
from time import sleep
import utime
import machine
import dht
import _thread

WIDTH  = 128                                            
HEIGHT = 64                                             
 

# CONSTANTS
KEY_UP   = const(0)
KEY_DOWN = const(1)
 
# Create a map between keypad buttons and characters
matrix_keys = [['1', '2', '3'],
               ['4', '5', '6'],
               ['7', '8', '9'],
               ['*', '0', '#']]
# PINs according to schematic - Change the pins to match with your connections
keypad_rows = [4,5,6,7]
keypad_columns = [8,9,10]



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
    for row in range(4):
        for col in range(3):
            row_pins[row].high()
            if col_pins[col].value() == 1:
                # Wait for a short debounce time (e.g., 10ms) and check the value again
                utime.sleep(0.01)
                if col_pins[col].value() == 1:
                    # Debounced button press, return the key
                    print(matrix_keys[row][col] )
                    return matrix_keys[row][col]
            
            row_pins[row].low()

    utime.sleep(0.05)
    return 'X'
 


def read_sensor_data():
    global temperature,humidity
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except Exception as e:
        return None, None


i2c = I2C(0,scl=Pin(1), sda=Pin(0),freq = 400000) #Init i2c
oled=ssd1306.SSD1306_I2C(128,64,i2c,0x3c)
dht_sensor = dht.DHT11(Pin(16))
oled.text_encoding = 'utf-8'

kpress = 'X'
timer = 3600
misting_interval = 10
minimum_humidity = 30

pump_active = False
mist_current_time = 0
start_time = utime.ticks_ms()
current_time = utime.ticks_ms()

#Startup code that contains the initial code
def InitDevice():
           
    oled.fill(0)
    oled.text("ECOFOGGER", 0, 0)
    oled.text("Your Pets",0,16)
    oled.text("favorite gadget!", 0, 32)
    oled.text("Initiating...",0,48)
    oled.show()
    
    utime.sleep(2)
    
    oled.fill(0)
    oled.show()

def mainMenu():
    global setting_mode
    read_sensor_data()
    oled.fill(0)
    oled.text("Temp:{}°C".format(temperature), 0, 0)
    oled.text("Humidity:{}%".format(humidity), 0, 16)
    oled.show()
    
    kpress = scankeys()
   
    if kpress == '#':
        setting_mode = True
        
    utime.sleep(0.1)
    
def SettingMenu():
    global setting_mode
    global kpress
    oled.fill(0)
    
    oled.text("1 - Set Timer", 0, 0)
    oled.text("2 - Set Humidity", 0, 16)
    oled.text("3 - Set Interval", 0, 32)
    oled.text("* To Exit", 0, 64)
    
    oled.show()
    utime.sleep(0.1)
    kpress = scankeys()
     
   
        
    if kpress == '*':
        setting_mode = False
    elif kpress == '1':
        mistinginterval = GetValuesScreen()
    elif kpress == '2':
        minimum_humidity = GetValuesScreen()
    elif kpress == '3':
        mist_current_time = GetValuesScreen()
    
def MistScreen():
        oled.fill(0)
        oled.text("Misting...",0,16)
        oled.show()
    
def GetValuesScreen():
    
    global setting_mode
    global kpress
    current = ""
    done = False
    while not done:
        oled.fill(0)
        
        oled.text("Input value", 0, 0)
        oled.text("del->*, when",0,16)
        oled.text("done,press'#'", 0, 32)
        oled.text(current, 0, 48)
        oled.text("* To Exit", 0, 64)
        oled.show()
        utime.sleep(0.1)
        kpress = scankeys()
        
        if kpress == '*':
            current = current[:len(current)-1]
        elif kpress == '#':
            done = True
        elif kpress == 'X':
            done = False #so pao para isto n se merdar
        elif kpress != 'X':
            current = current + kpress
            
    return current

def min2MS(input):
    return (input * 60) * 1000

def Mist():
    a = 2
    b = a + a
    


def timeManaging():
    global current_time
    global start_time
    global misting_interval
    global Time_to_mist
    
    current_time = utime.ticks_ms()
    
    if current_time > start_time + min2MS(misting_interval):
        start_time = current_time
        Time_to_mist = True
        

###############MAIN CODE##########################
#init portion
setting_mode = False
Time_to_mist = False
misting_tip = False #"deixa"
InitDevice()
print("get ready")
#_thread.start_new_thread(timeManagingCore1, ())

#main loop
while True:
    timeManaging()
   
    if Time_to_mist: 
        Mist()
        MistScreen()

    if not setting_mode:
        mainMenu()
    else:
        SettingMenu()
    


