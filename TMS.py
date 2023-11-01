from machine import Pin,I2C
import ssd1306
from time import sleep
import utime
import machine
import dht


WIDTH  = 128                                            
HEIGHT = 64                                             
 
i2c = I2C(0,scl=Pin(1), sda=Pin(0),freq = 400000) #Init i2c
oled=ssd1306.SSD1306_I2C(128,64,i2c,0x3c)
dht_sensor = dht.DHT11(Pin(16))

oled.text_encoding = 'utf-8'


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
    global kpress
    kpress = None  # Reset kpress to None at the beginning of the function
    for row in range(4):
        for col in range(3):
            row_pins[row].high()
            
            if col_pins[col].value() == 1:
                print("You have pressed:", matrix_keys[row][col])
                kpress = matrix_keys[row][col]
                
                utime.sleep(0.3)  # Sleep for a short time to debounce
                row_pins[row].low()
                return kpress

        row_pins[row].low()

    return kpress  # Return kpress even if no key is pressed

 
timer = 3600
misting_interval = 15
minimum_humidity = 30
setting_mode = False
pump_active = False
mist_current_time = 0
start_time = utime.ticks_ms()



# Function to display temperature and humidity on the LCD
def display_data(temperature, humidity):
    oled.fill(0)
    oled.text("Temp: " + str(temperature) + " C", 0, 0)
    oled.text("Humidity: " + str(humidity) + "%", 0, 32)
    oled.show()

def read_sensor_data():
    global temperature,humidity
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except Exception as e:
        return None, None

def time2seconds(hh, mm):
    return (hh * 60 + mm) * 60

def clear_display():
    oled.fill(0)
    oled.show()

def update_display():
    read_sensor_data()
    oled.fill(0)
    oled.text("Temp:{}°C".format(temperature), 0, 0)
    oled.text("Humidity:{}%".format(humidity), 0, 16)

    if setting_mode:
        
        oled.text("1 - Set Timer", 0, 48)
        oled.text("2 - Set Humidity", 0, 56)
        oled.text("3 - Set Interval", 0, 64)
        oled.text("* To Exit", 0, 72)
    else:
        oled.text("Min Humidity:{}%".format(minimum_humidity), 0, 48)
        oled.show()

    if pump_active:
        oled.text("Misting...", 80, 48)
        oled.show()

    oled.show()

def setTimer():
    global timer
    hh = 0
    mm = 0
    editing_hours = True
    kpress = None
    previous_kpress = None  # Store the previous keypress

    while True:
        oled.fill(0)
        oled.text("Set the timer (hh:mm)", 0, 0)

        time_str = str(hh // 10) + str(hh % 10) + ":" + str(mm // 10) + str(mm % 10)
        oled.text(time_str, 48, 24)
        oled.show()

        kpress = scankeys()  # Assign the result of scankeys to kpress

        if kpress is not None:
            if kpress == "#":
                setting_mode = False
                timer = time2seconds(hh, mm)
                break
            elif kpress == "*":
                setting_mode = False
                break
            elif kpress.isdigit():
                # Handle digits
                if editing_hours:
                    hh = int(str(hh % 10) + kpress)  # Update the hour part
                    hh = min(23, hh)  # Ensure hours stay within 0-23
                else:
                    mm = int(str(mm % 10) + kpress)  # Update the minute part
                    mm = min(59, mm)  # Ensure minutes stay within 0-59
                editing_hours = not editing_hours
        elif previous_kpress is not None:
            kpress = previous_kpress  # Restore previous keypress
        previous_kpress = kpress



def setMistingInterval():
    global misting_interval
    ss = 0

    while True:
        oled.fill(0)
        oled.text("Set the interval (ss)", 0, 0)

        ss_str = str(ss // 10) + str(ss % 10)
        oled.text(ss_str, 64, 24)
        oled.show()

        kpress = scankeys()

        if kpress == "#":
            # Exit and save the interval setting
            misting_interval = ss
            break
        elif kpress == "*":
            # Exit without saving
            break
        elif kpress.isdigit():
            # Handle digits
            ss = int(press)
            ss %= 60  # Ensure seconds stay within 0-59

def setMinimumHumidity():
    global minimum_humidity
    humidity = 50  # Default value, change it if needed

    while True:
        kpress = scankeys()
        oled.fill(0)
        oled.text("Set minimum humidity (%)", 0, 0)

        humidity_str = str(humidity) + "%"
        oled.text(humidity_str, 48, 24)
        oled.show()
        
        if kpress == "#":
            # Exit and save the minimum humidity setting
            minimum_humidity = humidity
            break
        elif kpress == "*":
            # Exit without saving
            break
        elif kpress.isdigit():
            # Handle digits
            humidity = int(kpress)
            humidity = max(0, min(100, humidity))  # Ensure humidity stays within 0-100

# MAIN LOOP -------------------------------------------------------------------------------------------

while True:
    update_display()
    kpress = scankeys()
    print(kpress)
    print("Kpress:",kpress)
    current_time = utime.ticks_ms()
    if current_time - start_time >= timer * 1000:  # Convert timer (seconds) to milliseconds
        if not pump_active:
            pump_active = True# Turn on the pump
            clear_display()
            relay.on()
            mist_start_time = current_time
        start_time = current_time  # Reset the start time

    # Check if it's time to turn off the pump
    if pump_active:
        mist_current_time = current_time
        if mist_current_time - mist_start_time >= misting_interval * 1000:
            pump_active = False  # Turn off the pump
            clear_display()
            relay.off()
            

    else:
        if kpress == "#":
            if setting_mode:
                clear_display()
                setting_mode = False
                update_display()
            else:
                clear_display()
                setting_mode = True
                update_display()
        elif kpress == "*":
            if setting_mode:
                clear_display()
                setting_mode = False
                update_display()
        elif kpress == "1":
            if setting_mode:
                clear_display()
                setTimer()
        elif kpress == "2":
            if setting_mode:
                clear_display()
                setMistingInterval()
        elif kpress == "3":
            if setting_mode:
                clear_display()
                setMinimumHumidity() 
        else:
            update_display()
