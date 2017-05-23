# Simple script to demonstrate controlling a Galcon 9001BT valve
#
#https://github.com/suborb/GalconController

import binascii
import struct
import sys
from bluepy import btle

perip = btle.Peripheral(sys.argv[1])

# Needed to wake up device to get the right result
status = perip.getCharacteristics(uuid = "e86802019c4b11e4b5f70002a5d5c51b")[0]
value= status.write(bytes("\x01\x02","utf-8"))

# Read the status
status = perip.getCharacteristics(uuid = "e86801029c4b11e4b5f70002a5d5c51b")[0]
value = status.read()
print(value)

# Irrigation control - valve on
status = perip.getCharacteristics(uuid = "e86801039c4b11e4b5f70002a5d5c51b")[0]
value= status.write(bytes("\x00\x01\x00\x00\x00\x00\x00","utf-8"))

# Read the status
status = perip.getCharacteristics(uuid = "e86801029c4b11e4b5f70002a5d5c51b")[0]
value = status.read()
print(value)

# Irrigation control - valve off
status = perip.getCharacteristics(uuid = "e86801039c4b11e4b5f70002a5d5c51b")[0]
value= status.write(bytes("\x01\x00\x00\x00\x00\x00\x00","utf-8"))

# Read the status
status = perip.getCharacteristics(uuid = "e86801029c4b11e4b5f70002a5d5c51b")[0]
value = status.read()
print(value)


# Send pin code - all pairing is handled on the client side, so it's pointless
# pairing
#status = perip.getCharacteristics(uuid = "e86804019c4b11e4b5f70002a5d5c51b")[0]
#value= status.write(bytes("\x01\x02\x03\x04","utf-8"))

