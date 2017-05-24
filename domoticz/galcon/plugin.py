"""
<plugin key="galcon" name="Galcon Irrigation Controller" author="suborb" version="1.0.0" wikilink="http://github.com/suborb/GalconController">
    <params>
        <param field="Address" label="Bluetooth Address" width="200px" required="true" default="00:00:00:00:00:00"/>
    </params>
</plugin>

"""
import time
import sys
import Domoticz
sys.path.append("/usr/local/lib/python3.4/dist-packages/")
from bluepy import btle

device = None
controlCharacteristic = None
statusCharacteristic = None
lastTime = 0


def onStart():
    if (len(Devices) == 0):
        Domoticz.Device(Name="Status",  Unit=1, TypeName="Switch").Create()
    if GalconConnect() == False:
        Domoticz.Error("Failed to establish connection to device, will try again in a bit");
    return True


def GalconConnect():
    global device
    global controlCharacteristic
    global statusCharacteristic
    Domoticz.Log("Attempting to connect to " + Parameters["Address"])
    device = None
    success = False
    count = 0
    while success == False and count < 3:
        try:
            device = btle.Peripheral(Parameters["Address"])
            controlCharacteristic = device.getCharacteristics(uuid = "e86801039c4b11e4b5f70002a5d5c51b")[0]
            statusCharacteristic = device.getCharacteristics(uuid = "e86801029c4b11e4b5f70002a5d5c51b")[0]
            Domoticz.Log("Connected to " + Parameters["Address"])
            return True
        except btle.BTLEException:
            device = None
    return False


def onConnect(Status, Description):
    return True

def onMessage(Data):
    return True

def onCommand(Unit, Command, Level, Hue):
    global controlCharacteristic
    global device
    global lastTime
    Command = Command.strip()
    action, sep, params = Command.partition(' ')
    action = action.capitalize()

    success = False
    count = 0
    if device == None and GalconConnect() == False:
        Domoticz.Error("Failed to connect not executing command!")
        return

    success = False
    count = 0
    while success == False and count < 5:
        try:
            if action == 'On':
                controlCharacteristic.write(bytes("\x00\x01\x00\x00\x00\x00\x00","utf-8"))
                UpdateDevice(1, 1, '')
            if action == 'Off':
                controlCharacteristic.write(bytes("\x01\x00\x00\x00\x00\x00\x00","utf-8"))
                UpdateDevice(1, 0, '')
            Domoticz.Log("Switched successfully")
            lastTime = time.time() - 295
            success = True
        except btle.BTLEException:
            device.disconnect()
            GalconConnect()
    return True

def onNotification(Data):
    Domoticz.Log("Notification: " + str(Data))
    return

def onHeartbeat():
    global lastTime
    global statusCharacteristic
    global device
    now = time.time()
    if device == None and GalconConnect() == False:
        Domoticz.Error("Failed to connect - can't poll status!")
        return True
    if now - lastTime >= 300:
        try:
            status = statusCharacteristic.read()
            if status[0] & 1 != 0:
                UpdateDevice(1, 1, '')
            else:
                UpdateDevice(1, 0, '') 
            lastTime = now
        except btle.BTLEException:
            device.disconnect()
            GalconConnect()
    return True

def onDisconnect():
    return
   

def onStop():
    Domoticz.Log("onStop called")
    return True


def UpdateDevice(Unit, nValue, sValue):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue):
            Devices[Unit].Update(nValue, str(sValue))
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return
