from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import dht
import time

# Initialize I2C for the OLED display
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# Create an SSD1306 instance for your OLED display
oled = SSD1306_I2C(128, 64, i2c)

# Initialize the DHT22 sensor
dht_sensor = dht.DHT22(Pin(2))  # Replace with the appropriate GPIO pin for the DHT22 sensor

# Initialize the 5V relay for controlling the 12V pump
relay = Pin(16, Pin.OUT)

# Initialize the keypad
# Connect your 3x4 matrix keypad to the appropriate GPIO pins
# Configure keypad mapping as needed
keypad = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]
rows = [Pin(4, Pin.IN, Pin.PULL_UP), Pin(5, Pin.IN, Pin.PULL_UP), Pin(6, Pin.IN, Pin.PULL_UP), Pin(7, Pin.IN, Pin.PULL_UP)]
cols = [Pin(8, Pin.OUT), Pin(9, Pin.OUT), Pin(10, Pin.OUT), Pin(11, Pin.OUT)]

# Initialize the state variables
pump_active = False
setting_mode = False  # Setting mode to access timer, humidity, and interval settings
timer_hours = 0
timer_minutes = 0
minimum_humidity = 50
misting_interval = 60

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

while True:
    temperature, humidity = read_sensor_data()

    # Handle keypad input
    keys = read_keypad()
    if not any(keys):
        pass  # No keys are pressed
    else:
        key = keypad[keys[0]][keys[1]]
        if key == "#":
            if setting_mode:
                setting_mode = False
                update_display()
            else:
                setting_mode = True
                update_display()
        elif key == "*":
            # Exit setting mode
            if setting_mode:
                setting_mode = False
                update_display()
        elif setting_mode:
            if key == "1":
                # Enter timer setting mode
                timer_hours = 0
                timer_minutes = 0
                update_display()
            elif key == "2":
                # Enter humidity setting mode
                minimum_humidity = 50
                update_display()
            elif key == "3":
                # Enter interval setting mode
                misting_interval = 60
                update_display()
        elif key.isdigit():
            # Handle numeric input during setting modes
            if setting_mode:
                if key == "1":
                    timer_hours = timer_hours * 10 + int(key)
                elif key == "2":
                    timer_minutes = timer_minutes * 10 + int(key)
                elif key == "3":
                    minimum_humidity = minimum_humidity * 10 + int(key)
                elif key == "4":
                    misting_interval = misting_interval * 10 + int(key)
        elif setting_mode and key == "#":
            # Confirm changes and exit setting mode
            setting_mode = False
            update_display()
        update_display()
    
    update_display