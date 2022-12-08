# usage => cd /boot/deviceSDK && python3 SenseHatPubSubAws.py
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import RPi.GPIO as GPIO
import time
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import json

# Sense hat 8x8 LED matrix colour definitions
ColourR = [150, 0, 0]  # Red
ColourG = [0, 150, 0] # Green
ColourB = [0, 0, 150] # Blue
ColourW = [50, 50, 50]  # White
ColourGr = [15, 15, 15] # GrayG
ColourBk = [0, 0, 0] # Black
ColourY = [75, 75, 0] # yellow
ColourM = [75, 0, 75] # magenta
ColourC = [0, 75, 75] # cyan

#Sense hat object instantiation
sense = SenseHat()

#Boot Messages MQTT Pub Sub AWS
sense.show_message("Boot Rpi", text_colour = ColourB, back_colour = ColourBk)


# A random programmatic shadow client ID.
SHADOW_CLIENT = "myShadowClient"
# The unique hostname that AWS IoT generated for
# this device.
#HOST_NAME = "arn:aws:iot:us-east-2:486589451357:thing/AlumnusRpi"
#HOST_NAME = "ALS-IEM-ats.iot.us-east-2.amazonaws.com"
HOST_NAME = "a6c7b7fj95byi-ats.iot.us-east-2.amazonaws.com"
# The relative path to the correct root CA file for AWS IoT,
# that you have already saved onto this device.
ROOT_CA = "AmazonRootCA1.pem.txt"
# The relative path to your private key file that
# AWS IoT generated for this device, that you
# have already saved onto this device.
PRIVATE_KEY = "558813dae2-private.pem.key"
# The relative path to your certificate file that
# AWS IoT generated for this device, that you
# have already saved onto this device.
CERT_FILE = "558813dae2-certificate.pem.crt"
# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "AlumnusRpi"

# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
    print()
    print('UPDATE: $aws/things/' + SHADOW_HANDLER + '/shadow/update/#')
    print("payload = " + payload)
    print("responseStatus = " + responseStatus)
    print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(30)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(SHADOW_HANDLER, True)

# Represents the GPIO27 pin - Push button is connected
channelIn = 27

# Represents the GPIO17 pin - LED is connected
channelOut = 17

# Use the GPIO BCM pin numbering scheme.
GPIO.setmode(GPIO.BCM)

# Receive input signals through the pin.
GPIO.setup(channelIn, GPIO.IN)

# Send output signals through the pin.
GPIO.setup(channelOut, GPIO.OUT)

# Initialize first values of button
currentButtonValue = 1
previousButtonValue = 1

# Initialize first values of temperature
currentTemperatureValue = 0
previousTemperatureValue = 0

# Initialize first values of humidity
currentHumidityValue = 0
previousHumidityValue = 0

# Initialize first values of pressure
currentPressureValue = 0
previousPressureValue = 0

# Acclerometer values
xCurrentAccnInG = 0
yCurrentAccnInG = 0
zCurrentAccnInG = 0
xPreviousAccnInG = 0
yPreviousAccnInG = 0
zPreviousAccnInG = 0


# Boot Messages MQTT Pub Sub AWS
sense.show_message("M", text_colour = ColourW, back_colour = ColourBk)
sense.show_message("Q", text_colour = ColourR, back_colour = ColourBk)
sense.show_message("T", text_colour = ColourG, back_colour = ColourBk)
sense.show_message("T", text_colour = ColourB, back_colour = ColourBk)
sense.show_message("Pub", text_colour = ColourY, back_colour = ColourBk)
sense.show_message("Sub", text_colour = ColourM, back_colour = ColourBk)
sense.show_message("AWS", text_colour = ColourC, back_colour = ColourBk)

# Function LIGHT ON
def LightOn():
    sense.set_pixel(0, 0, ColourY)
    sense.set_pixel(0, 1, ColourY)
    sense.set_pixel(0, 2, ColourY)
    sense.set_pixel(1, 2, ColourY)
    sense.set_pixel(3, 0, ColourY)
    sense.set_pixel(3, 1, ColourY)
    sense.set_pixel(3, 2, ColourY)
    sense.set_pixel(5, 0, ColourY)
    sense.set_pixel(6, 0, ColourY)
    sense.set_pixel(7, 0, ColourY)
    sense.set_pixel(6, 1, ColourY)
    sense.set_pixel(6, 2, ColourY)

# Function LIGHT OFF
def LightOff():
    sense.set_pixel(0, 0, ColourBk)
    sense.set_pixel(0, 1, ColourBk)
    sense.set_pixel(0, 2, ColourBk)
    sense.set_pixel(1, 2, ColourBk)
    sense.set_pixel(3, 0, ColourBk)
    sense.set_pixel(3, 1, ColourBk)
    sense.set_pixel(3, 2, ColourBk)
    sense.set_pixel(5, 0, ColourBk)
    sense.set_pixel(6, 0, ColourBk)
    sense.set_pixel(7, 0, ColourBk)
    sense.set_pixel(6, 1, ColourBk)
    sense.set_pixel(6, 2, ColourBk)

# Function AC ON
def ACOn():
    sense.set_pixel(1, 4, ColourR)
    sense.set_pixel(0, 5, ColourR)
    sense.set_pixel(2, 5, ColourR)
    sense.set_pixel(0, 6, ColourR)
    sense.set_pixel(1, 6, ColourR)
    sense.set_pixel(2, 6, ColourR)
    sense.set_pixel(0, 7, ColourR)
    sense.set_pixel(2, 7, ColourR)

# Function AC OFF
def ACOff():
    sense.set_pixel(1, 4, ColourG)
    sense.set_pixel(0, 5, ColourG)
    sense.set_pixel(2, 5, ColourG)
    sense.set_pixel(0, 6, ColourG)
    sense.set_pixel(1, 6, ColourG)
    sense.set_pixel(2, 6, ColourG)
    sense.set_pixel(0, 7, ColourG)
    sense.set_pixel(2, 7, ColourG)

# Function FAN ON
def FanOn():
    sense.set_pixel(5, 4, ColourR)
    sense.set_pixel(6, 4, ColourR)
    sense.set_pixel(7, 4, ColourR)
    sense.set_pixel(5, 5, ColourR)
    sense.set_pixel(5, 6, ColourR)
    sense.set_pixel(6, 6, ColourR)
    sense.set_pixel(5, 7, ColourR)

# Function FAN OFF
def FanOff():
    sense.set_pixel(5, 4, ColourG)
    sense.set_pixel(6, 4, ColourG)
    sense.set_pixel(7, 4, ColourG)
    sense.set_pixel(5, 5, ColourG)
    sense.set_pixel(5, 6, ColourG)
    sense.set_pixel(6, 6, ColourG)
    sense.set_pixel(5, 7, ColourG)

# Sense Hat Clear
sense.clear()

# Light On at start
LightOn()
LightState = "off"
# Fan Off at start
FanOff()
FanState = "off"
# AC off at start
ACOff()
AcState = "off"

# Wait 2 seconds
time.sleep(2)

# Sense Hat Clear
sense.clear()

# Retrieve the MQTTClient(MQTT connection) to perform plain MQTT operations along with shadow operations
myMQTTClient = myShadowClient.getMQTTConnection()
# Publish Power ON
valueToPrint = "Power ON"
nameValue = {"Raspberrry Pi 3 B+ with Sense Hat":valueToPrint}
jsonText = json.dumps(nameValue)
myMQTTClient.publish("$aws/things/" + SHADOW_HANDLER + "/shadow/update", jsonText, 1)

# Function Set Light State on
def LightStateSetOn(client, userdata, message):
    global LightState
    LightOn()
    LightState = "on"
    print("Received: LIGHT ON")
    #  print("message = " + json.dumps(message))
# Function Set Light State off
def LightStateSetOff(client, userdata, message):
    global LightState
    LightOff()
    LightState = "off"
    print("Received: LIGHT OFF")
    # print("message = " + json.dumps(message))
# Subscribe to Light On topic
myMQTTClient.subscribe("LightOn", 0, LightStateSetOn)
# Wait 1 second
time.sleep(1)
# Subscribe to Light Off topic
myMQTTClient.subscribe("LightOff", 0, LightStateSetOff)
# Wait 1 second
time.sleep(1)

# Function Set Fan State on
def FanStateSetOn(client, userdata, message):
    global FanState
    FanOn()
    FanState = "on"
    print("Received: FAN ON")
    #  print("message = " + json.dumps(message))
# Function Set Fan State off
def FanStateSetOff(client, userdata, message):
    global FanState
    FanOff()
    FanState = "off"
    print("Received: FAN OFF")
    # print("message = " + json.dumps(message))
# Subscribe to Fan On topic
myMQTTClient.subscribe("FanOn", 0, FanStateSetOn)
# Wait 1 second
time.sleep(1)
# Subscribe to Fan Off topic
myMQTTClient.subscribe("FanOff", 0, FanStateSetOff)
# Wait 1 second
time.sleep(1)

# Function Set AC State on
def AcStateSetOn(client, userdata, message):
    global AcState
    ACOn()
    AcState = "on"
    print("Received: AC ON")
    #  print("message = " + json.dumps(message))
# Function Set AC State off
def AcStateSetOff(client, userdata, message):
    global AcState
    ACOff()
    AcState = "off"
    print("Received: AC OFF")
    # print("message = " + json.dumps(message))
# Subscribe to AC On topic
myMQTTClient.subscribe("AcOn", 0, AcStateSetOn)
# Wait 1 second
time.sleep(1)
# Subscribe to AC Off topic
myMQTTClient.subscribe("AcOff", 0, AcStateSetOff)
# Wait 1 second
time.sleep(1)

# Infinite loop to keep this script running.
while True:
    # Wait for 2  seconds
    time.sleep(2)
    # Read sense hat temperature on bord
    currentTemperatureValue = sense.get_temperature()
    # Publish temperature if 1 degree C difference with previous reading
    if (abs(currentTemperatureValue-previousTemperatureValue) > 1.0):
        previousTemperatureValue = currentTemperatureValue
        valueToPrint = float("{0:.2f}".format(currentTemperatureValue))
        senseName = "Temperature = "
        senseUnit = " degree C "
        print(senseName + str(valueToPrint) + senseUnit)
        sense.clear()
        nameValue = {"state":{"reported":{"TEMPERATURE(degree C)":valueToPrint}}}
        jsonText = json.dumps(nameValue)
        myDeviceShadow.shadowUpdate(jsonText, myShadowUpdateCallback, 5)
    # Read sense hat humidity on board
    currentHumidityValue = sense.get_humidity()
    # Publish humidity if 10% change with respect to previous value
    if (abs(currentHumidityValue-previousHumidityValue) > 10.0):
        previousHumidityValue = currentHumidityValue
        valueToPrint = float("{0:.2f}".format(currentHumidityValue))
        senseName = "Humidity = "
        senseUnit = " % "
        print(senseName + str(valueToPrint) + senseUnit)
        sense.clear()
        nameValue = {"state":{"reported":{"HUMIDITY(%)":valueToPrint}}}
        jsonText = json.dumps(nameValue)
        myDeviceShadow.shadowUpdate(jsonText, myShadowUpdateCallback, 5)
    # Read sense hat pressure on board
    currentPressureValue = sense.get_pressure()
    # Publish pressure if 1 milli bar change with respect to previous value
    if (abs(currentPressureValue-previousPressureValue) > 1.0):
        previousPressureValue = currentPressureValue
        valueToPrint = float("{0:.2f}".format(currentPressureValue))
        senseName = "Pressure = "
        senseUnit = " milli bar "
        print(senseName + str(valueToPrint) + senseUnit)
        sense.clear()
        nameValue = {"state":{"reported":{"PRESSURE(milli bar)":valueToPrint}}}
        jsonText = json.dumps(nameValue)
        myDeviceShadow.shadowUpdate(jsonText, myShadowUpdateCallback, 5)
    # Reade sense Hat Joystick events
    for event in sense.stick.get_events():
        # Publish if Joysick released only
        if event.action == ACTION_RELEASED:
            if event.direction == "up":
                myDeviceShadow.shadowUpdate('{"state":{"reported":{"JOYSTICK":"EVENT UP"}}}',myShadowUpdateCallback, 5)
            if event.direction == "down":
                myDeviceShadow.shadowUpdate('{"state":{"reported":{"JOYSTICK":"EVENT DOWN"}}}',myShadowUpdateCallback, 5)
            if event.direction == "left":
                myDeviceShadow.shadowUpdate('{"state":{"reported":{"JOYSTICK":"EVENT LEFT"}}}',myShadowUpdateCallback, 5)
            if event.direction == "right":
                myDeviceShadow.shadowUpdate('{"state":{"reported":{"JOYSTICK":"EVENT RIGHT"}}}',myShadowUpdateCallback, 5)
            if event.direction == "middle":
                myDeviceShadow.shadowUpdate('{"state":{"reported":{"JOYSTICK":"EVENT MIDDLE"}}}',myShadowUpdateCallback, 5)
        print("The joystick was {} {}".format(event.action, event.direction))
    # Read Sense Hat  Acclerometer
    acceleration = sense.get_accelerometer_raw()
    xCurrentAccnInG = acceleration['x']
    yCurrentAccnInG = acceleration['y']
    zCurrentAccnInG = acceleration['z']
    # Round off till two decimal places
    xCurrentAccnInG = round(xCurrentAccnInG, 1)
    yCurrentAccnInG = round(yCurrentAccnInG, 1)
    zCurrentAccnInG = round(zCurrentAccnInG, 1)
    # Publish if any (x, y or z) direction accleration value change is greater than equal to 0.5 g
    if (abs(xCurrentAccnInG-xPreviousAccnInG) >= 0.5 or abs(yCurrentAccnInG-yPreviousAccnInG) >= 0.5 or abs(zCurrentAccnInG-zPreviousAccnInG) >= 0.5):
        xPreviousAccnInG  =  xCurrentAccnInG
        yPreviousAccnInG  =  yCurrentAccnInG
        zPreviousAccnInG  =  zCurrentAccnInG
        # Print
        print("x=%s, y=%s, z=%s" % (xCurrentAccnInG, yCurrentAccnInG, zCurrentAccnInG))
        sense.clear()
        nameValue = {"state":{"reported":{"AccX(g)":xCurrentAccnInG, "AccY(g)":yCurrentAccnInG, "AccZ(g)":zCurrentAccnInG}}}
        jsonText = json.dumps(nameValue)
        myDeviceShadow.shadowUpdate(jsonText, myShadowUpdateCallback, 5)
    # Control Light
    if(LightState == "on"):
        LightOn()
    if(LightState == "off"):
        LightOff()
    # Control Fan
    if(FanState == "on"):
        FanOn()
    if(FanState == "off"):
        FanOff()
    # Control AC
    if(AcState == "on"):
        ACOn()
    if(AcState == "off"):
        ACOff()

# Clean things up if for any reason we get to this
# point before script stops.
GPIO.cleanup()
