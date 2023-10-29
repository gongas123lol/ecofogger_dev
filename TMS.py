    from machine import Pin, I2C
    from ssd1306 import SSD1306_I2C
    import dht
    import utime

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
    
    
    # Time variables
    timer = 3600
    minimum_humidity = 50
    misting_interval = 60
    mist_current_time = 0
    start_time = utime.ticks_ms()

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

    def clear_display():
        oled.fill(0)
        oled.show()

    def update_display():
        oled.fill(0)
        oled.text("Temp:", str(temperature), "ºC" 0, 0)
        oled.text("Humidity:", str(humidity),"%", 0, 16)
        
        if setting_mode:
            clear_display()
            oled.text("1 - Set Timer", 0, 48)
            oled.text("2 - Set Humidity", 0, 56)
            oled.text("3 - Set Interval", 0, 64)
            oled.text("* To Exit", 0, 72)
        else:
            clear_display()
            oled.text("Min Humidity:", str(minimum_humidity),"%", 0, 48)
            oled.show()

        if pump_active:
            clear_display()
            oled.text("Misting...", 80, 48)
            oled.show()
            
        oled.show()

    def setTimer():
    global timer
    hh = 0
    mm = 0
    editing_hours = True

    while True:
        oled.fill(0)
        oled.text("Set the timer (hh:mm)", 0, 0)

        time_str = str(hh // 10) + str(hh % 10) + ":" + str(mm // 10) + str(mm % 10)
        oled.text(time_str, 48, 24)
        oled.show()

        keys = read_keypad()
        if not any(keys):
            continue

        key = keypad[keys[0]][keys[1]]

        if key == "#":
            # Exit and save the timer setting
            timer = time2seconds(hh, mm)
            break
        elif key == "*":
            # Exit without saving
            break
        elif key == "0" or key.isdigit():
            # Handle digits
            if editing_hours:
                hh = int(key)
            else:
                mm = int(key)
                mm %= 60  # Ensure minutes stay within 0-59
            editing_hours = not editing_hours


def setMistingInterval():
    global misting_interval
    ss = 0

    while True:
        oled.fill(0)
        oled.text("Set the interval (ss)", 0, 0)

        ss_str = str(ss // 10) + str(ss % 10)
        oled.text(ss_str, 64, 24)
        oled.show()

        keys = read_keypad()
        if not any(keys):
            continue

        key = keypad[keys[0]][keys[1]]

        if key == "#":
            # Exit and save the interval setting
            misting_interval = ss
            break
        elif key == "*":
            # Exit without saving
            break
        elif key.isdigit():
            # Handle digits
            ss = int(key)
            ss %= 60  # Ensure seconds stay within 0-59
            
            
            
            
def setMinimumHumidity():
    global minimum_humidity
    humidity = 50  # Default value, change it if needed

    while True:
        oled.fill(0)
        oled.text("Set minimum humidity (%)", 0, 0)

        humidity_str = str(humidity) + "%"
        oled.text(humidity_str, 48, 24)
        oled.show()

        keys = read_keypad()
        if not any(keys):
            continue

        key = keypad[keys[0]][keys[1]]

        if key == "#":
            # Exit and save the minimum humidity setting
            minimum_humidity = humidity
            break
        elif key == "*":
            # Exit without saving
            break
        elif key.isdigit():
            # Handle digits
            humidity = int(key)
            humidity = max(0, min(100, humidity))  # Ensure humidity stays within 0-100
            

# MAIN LOOP -------------------------------------------------------------------------------------------

    while True:
        current_time = utime.ticks_ms()
    if current_time - start_time >= timer * 1000:  # Convert timer (seconds) to milliseconds
        if not pump_active:
            pump_active = True  # Turn on the pump
            relay.on()
            mist_start_time = current_time
        start_time = current_time  # Reset the start time

    # Check if it's time to turn off the pump
    if pump_active:
        mist_current_time = current_time
        if mist_current_time - mist_start_time >= misting_interval * 1000:
            pump_active = False  # Turn off the pump
            relay.off()
        
        
        keys = read_keypad()
        
        if not any(keys):
            pass
        else:
            key = keypad[keys[0]keys[1]]
            if key == "#":
                if setting_mode:
                    setting_mode = False
                    update_display()
                else:
                setting_mode = True
                update_display()
            elif key == "*":
                if setting_mode:
                    setting_mode = false
                    update_display()
            elif key == "1":
                if setting_mode:
                    clear_display()
                    setTimer()
            elif key == "2":
                if setting_mode:
                    clear_display()
                    setInterval()
                
            elif key == "3":
                if setting_mode:
                    clear_display()
                    setMinimumHumidity()
        
        
        
        

        update_display()

