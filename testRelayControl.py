#!/usr/bin/env python
# testRelayControl - Program to test the usbRelayControl function
# by Sean Clay
# Rev. 1.0.0 - 12/15/2015

from usbRelayControl import relayOn, relayOff
import time
import sys
import serial

# This turns relays from 1 to 8 on and off
i = 1
while i < 9:
    print (i)
    relayOn([i])
    time.sleep(1)
    relayOff([i])
    i = i + 1

# This turns on all 8 relays and then turns off odd ones then even ones
relayOn([1, 2, 3, 4, 5, 6, 7, 8])
time.sleep(1)
relayOff([1, 3, 5, 7])
time.sleep(1)
relayOff([2, 4, 6, 8])
