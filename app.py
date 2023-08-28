from flask import Flask, render_template, request
import spidev
import math

# SPI setup
spi_bus = 0  # Change the SPI bus number if necessary
spi_device = 0  # Change the SPI device number if necessary
spi_speed_hz = 1000000  # Change the SPI clock speed if necessary

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Send a message over SPI
def send_message_over_spi(message):
    try:
        spi = spidev.SpiDev()
        spi.open(spi_bus, spi_device)
        spi.max_speed_hz = spi_speed_hz

        spi.writebytes(list(message.encode()))
        print("Message sent:", message)
    except IOError as e:
        print("SPI error:", e)
    finally:
        spi.close()

@app.route('/command', methods=['POST'])
def handle_command():
    velRobot = 0.3
    thetaRobot = 0.0000
    omegaRobot = 0
    
    direction = request.json['direction']
    # Add your desired functionality here based on the received direction
    if(direction[0:13] == ":move:forward"):
        if(direction == ":move:forward;"):
            thetaRobot = 0.0000
        elif(direction == ":move:forward:right;"):
            thetaRobot = 7*math.pi/4
        elif(direction == ":move:forward:left;"):
            thetaRobot = math.pi/4
        else:
            print("Comando forward desconocido")
                  
    elif(direction[0:14] == ":move:backward"):
        if(direction == ":move:backward;"):
            thetaRobot = math.pi
        elif(direction == ":move:backward:right;"):
            thetaRobot = 5*math.pi/4
        elif(direction == ":move:backward:left;"):
            thetaRobot = 3*math.pi/4
        else:
            print("Comando backward desconocido")
    
    elif(direction[0:11] == ":move:right"):
        if(direction == ":move:right;"):
            thetaRobot = 3*math.pi/2
        else:
            print("Comando right desconocido")

    elif(direction[0:10] == ":move:left"):
        if(direction == ":move:left;"):
            thetaRobot = math.pi/2
        else:
            print("Comando left desconocido")
    
    elif(direction[0:10] == ":move:stop"):
        if(direction == ":move:stop;"):
            thetaRobot = 0.0000
            velRobot = 0.0
        else:
            print("Comando stop desconocido")
    
    elif(direction[0:8] == ":rotate:"):
        if(direction == ":rotate:CCW;"):
            omegaRobot = -1
        elif(direction == ":rotate:CW;"):
            omegaRobot = 1
        else:
            print("Comando rotate desconocido")

    # Execute the function
    if(thetaRobot == 0 and velRobot == 0): 
        send_message_over_spi(":00000:0:0;")
    elif(round(thetaRobot*10000) == 7854):
        send_message_over_spi(":07854:" + str(round(velRobot*10)) + ":0;")
    elif(thetaRobot == 0 and velRobot != 0 and omegaRobot == 0):
        send_message_over_spi(":00000:" + str(round(velRobot*10)) + ":0;")
    elif(velRobot != 0 and omegaRobot != 0 and omegaRobot == 1):
        send_message_over_spi(":00000:0:1;")
    elif(velRobot != 0 and omegaRobot != 0 and omegaRobot == -1):
        send_message_over_spi(":00000:0:2;")
    else:
        send_message_over_spi((":" + str(round(thetaRobot*10000)) + ":" + str(round(velRobot*10)) + ":0;"))
        
    print('Command received:', direction)
    print("Direction: ", thetaRobot)
    return 'Command received'

if __name__ == '__main__':
    app.run(host='192.168.4.1', port=5000)