#!/usr/bin/env python
# Cemetery Creeps - Halloween 2015
# by Sean Clay
# Rev. 1.2.0 - 10/30/2015

''' This program is designed for use on a Raspberry Pi computer
    and makes use of the computer's GPIO pins. Two skeleton dogs
    and a skeleton child are contolled by a separate Efx-Tek controller
    triggered by Relay #8 (no voltage). Two skeleton cats are triggered
    by Relays #5 & #6 and the rat is triggered by Relay #7 (no voltage)
    The main skeleton is controlled by a separate Efx-Tek controller
    and will stop and 'talk' when triggered by Relay#4 (no voltage).
    The fog machine and strobe for the Monster In Box is triggered
    by Relay #1 (12v). The fog machine is triggered by the strobe light.'''

# Initialize
import pygame
import time
import sys
import serial
import RPi.GPIO as GPIO
from pylibftdi import BitBangDevice

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)


def triggerMonsterBox():
    ''' Function to trigger Monster in a Box '''
    pygame.mixer.music.stop()
    relay_on(fog_strobe)
    print ("Strobe & Fog on!")
    pygame.init()
    pygame.mixer.music.load(monster_talk[1])
    pygame.mixer.music.play()
    print ("Playing Monster Box Sound Effects")
    time.sleep(8)
    relay_off(fog_strobe)
    print ("Stop Fog & Strobe!")
    pygame.mixer.music.stop()
    time.sleep(8)
    print ("Done with playing Monster Box sound")


def triggerCats():
    ''' Function to trigger the two cats '''
    relay_on(cat1)
    print ("Cat #1 Activated!")
    relay_on(cat2)
    print ("Cat #2 Activated!")
    time.sleep(3)
    print ("Cat #1 Deactivated!")
    relay_off(cat1)
    print ("Cat #2 Deactivated!")
    relay_off(cat2)


def triggerRat():
    ''' Function to trigger the rat '''
    relay_on(rat)
    print ("Rat Activated!")
    time.sleep(6)
    print ("Rat Deactivated!")
    relay_off(rat)


def triggerDogs():
    ''' Function to trigger the two dogs '''
    relay_on(dogs)
    print ("Dogs Activated!")
    pygame.init()
    pygame.mixer.music.load(monster_talk[0])
    pygame.mixer.music.play()
    print ("Playing Dogs Barking Sound Effects")
    time.sleep(10)
    print ("Dogs Deactivated!")
    relay_off(dogs)


def relay_on(relay):
    ''' Function to turn on specified relay '''
    with BitBangDevice() as bb:
        bb.port |= relay


def relay_off(relay):
    ''' Function to turn off specified relay '''
    with BitBangDevice() as bb:
        bb.port &= ~relay


skeleton_talk = (['BewareMyCats.wav', 'BewareTheRats.wav',
                  'MyDogsLoveChildren.wav', 'BewareTheBeastInTheBox.wav'])
monster_talk = ['dogs_bark.wav', 'monster_sound.mp3']
print ("all relays off!")

relay_off(255)  # All Relays Off!

# Assign Relays - All accessed by binary numbers 1 - 128
fog_strobe = 1   # Relay #1 Strobe light & Fog machine (12v)
move_jaw = 4   # Relay #3 Move the Skeleton's Jaw while he talks
cat1 = 16  # Relay #5 Activate Cat1 (no voltage. Switch only!)
cat2 = 32  # Relay #6 Activate Cat2 (no voltage. Switch only!)
rat = 64  # Relay #7 Activate Rat  (no voltage. Switch only!)
dogs = 128  # Relay #8 Activate Dogs (no voltage. Switch only!)

max_talk = len(skeleton_talk)-1
talk = 0  # Counter for which 'skeleton talk' sound we are on
victim = 0
print ("Starting Main Loop...")

# Main Loop
while 1 == 1:
    try:
        # All Clear - No victims
        pygame.init()
        pygame.mixer.music.set_volume(1)
        if GPIO.input(PIR_PIN):
            victim = 1
            print ("We have a victim!!")

        if victim:
            talk = talk + 1

        if talk == 1:
            relay_on(move_jaw)
            time.sleep(2)
            print ("Beware my cats!")
            pygame.mixer.music.load(skeleton_talk[talk-1])
            print ("Loaded ", skeleton_talk[talk-1])
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            relay_off(move_jaw)
            triggerCats()
            time.sleep(1)  # time between next sound

        if talk == 2:
            relay_on(move_jaw)
            time.sleep(2)
            print ("Watch out for those rats!")
            pygame.mixer.music.load(skeleton_talk[talk-1])
            print ("Loaded ", skeleton_talk[talk-1])
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            relay_off(move_jaw)
            triggerRat()
            time.sleep(1)  # time between next sound

        if talk == 3:
            relay_on(move_jaw)
            time.sleep(2)
            print ("My dogs love children!")
            pygame.mixer.music.load(skeleton_talk[talk-1])
            print ("Loaded ", skeleton_talk[talk-1])
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            relay_off(move_jaw)
            triggerDogs()
            time.sleep(1)  # time between next sound

        if talk == 4:
            relay_on(move_jaw)
            time.sleep(2)
            print ("The monster in the box is hungry!")
            pygame.mixer.music.load(skeleton_talk[talk-1])
            print ("Loaded ", skeleton_talk[talk-1])
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            relay_off(move_jaw)
            triggerMonsterBox()
            time.sleep(1)  # time between next sound

        if talk > max_talk:
            talk = 0
            victim = 0

        if talk == 0:
            print ("Waiting for next victim....")
            time.sleep(2)  # time between victim detection

    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        break
print ("All done!")
