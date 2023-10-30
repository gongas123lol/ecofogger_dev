
#function that makes the webpage we are sending out to the client

def webpage(humidity, temperature, mistTime, toBeDisplayed ):
    #Template HTML
    html = f"""
    @page
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .form-container {
            display: flex;
            justify-content: center;
        }

            .form-container form {
                margin: 0 10px; /* Add some margin to separate the forms */
            }
    </style>
</head>
<body>
    <h1>EcoFogger</h1>

    <p>Current humidity: {humidity}</p>
    <p>Current Temperature: {temperature}</p>
    <p>Ñext Mist in: {mistTime}</p>
    <p> {toBeDisplayed}</p>
    <p></p>

    <div class="form-container">
        <form action="./1">
            <input type="submit" value="1" />
        </form>

        <form action="./2">
            <input type="submit" value="2" />
        </form>

        <form action="./3">
            <input type="submit" value="3" />
        </form>
    </div>


    <div class="form-container">
        <form action="./4">
            <input type="submit" value="4" />
        </form>

        <form action="./5">
            <input type="submit" value="5" />
        </form>

        <form action="./6">
            <input type="submit" value="6" />
        </form>
    </div>


    <div class="form-container">
        <form action="./7">
            <input type="submit" value="7" />
        </form>

        <form action="./8">
            <input type="submit" value="8" />
        </form>

        <form action="./9">
            <input type="submit" value="9" />
        </form>
    </div>
    <p></p>
    <div class="form-container">
        <form action="./settimer">
            <input type="submit" value="Set Timer" />
        </form>

        <form action="./humidity">
            <input type="submit" value="Set Humidity" />
        </form>

        <form action="./mistinterval">
            <input type="submit" value="Set misting Interval" />
        </form>
    </div>
    <p></p>
    <form action="./ok">
        <input type="submit" value="OK!" />
    </form>

  
</body>
</html>
"""
            
    return str(html)

#--------------------------------------------------------------------------------------
#function that handles all the comunication between the server and the client

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass

      match lang:
        case '/1':
            # do stuff
    
        case '/2':
              # do stuff
    
       case '/3':
             # do stuff
        
        case '/4':
              # do stuff
    
       case '/5':
             # do stuff
        case '/6':
              # do stuff
        case '/7':
              # do stuff
        case '/8':
              # do stuff
        case '/9':
              # do stuff
        case '/humidity':
              # do stuff
        case '/mistinterval':
              # do stuff
        case '/ok':
             # do stuff
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        temperature = pico_temp_sensor.temp
        html = webpage(humidity, temperature, mistTime, toBeDisplayed )
        client.send(html)
        client.close()
