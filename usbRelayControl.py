#!/usr/bin/env python
# usbRelayControl - Functions to control USB 8-Relay Board
# by Sean Clay
# Rev. 1.0.0 - 12/15/2015

''' This program is designed for use with a USB 8-Relay Board'''

# Initialize
from pylibftdi import BitBangDevice


def relayOn(relayList):
    ''' Function to turn on specified relay(s) passed in a list '''
    for item in relayList:
        if item in range(1, 9):
            relay = 2**(item-1)
            with BitBangDevice() as bb:
                bb.port |= relay


def relayOff(relayList):
    ''' Function to turn on specified relay(s) passed in a list '''
    for item in relayList:
        if item in range(1, 9):
            relay = 2**(item-1)
            with BitBangDevice() as bb:
                bb.port &= ~relay
