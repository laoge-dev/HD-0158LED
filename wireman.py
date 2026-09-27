# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import const

SE  = 16    # 1
AB  = 18    # 2
A3  = 31    # 3
A2  = 33    # 3
A1  = 35    # 5
A0  = 37    # 6
DG  = 13    # 8
CLK = 12    # 9
WE  = 7     # 10
DR  = 22    # 11
ALE = 29    # 12

def showV(red, green):
    lenofline = int(len(red) / const.SCREENWIDTH)
    for k in range(lenofline - const.SCREENHEIGHT + 1):
        onepageRed = []
        onepageGreen = []
        for i in range(const.SCREENWIDTH * const.SCREENHEIGHT):
            onepageRed.append(red[const.SCREENWIDTH * k + i])
            onepageGreen.append(green[const.SCREENWIDTH * k + i])
        process(onepageRed, onepageGreen)
        time.sleep(const.SLEEPTIME_MODE_V)

def showH(red, green):
    lenofline = int(len(red) / const.SCREENHEIGHT)
    for k in range(lenofline - const.SCREENWIDTH + 1):
        onepageRed = []
        onepageGreen = []
        for i in range(const.SCREENHEIGHT):
            for j in range(const.SCREENWIDTH):
                onepageRed.append(red[i * lenofline + j + k])
                onepageGreen.append(green[i * lenofline + j + k])
        process(onepageRed, onepageGreen)
        time.sleep(const.SLEEPTIME_MODE_H)

def process(onepageRed, onepageGreen):
    for r in range(const.SCREENHEIGHT):
        for _ in range(const.SCREENWIDTH):
            GPIO.output([DG,DR], GPIO.LOW)
            GPIO.output(DR, onepageRed.pop(0))
            GPIO.output(DG, onepageGreen.pop(0))
            GPIO.output(CLK, GPIO.HIGH)
            GPIO.output(CLK, GPIO.LOW)

        GPIO.output(A3, r & 1)
        GPIO.output(A2, r >> 1 & 1)
        GPIO.output(A1, r >> 2 & 1)
        GPIO.output(A0, r >> 3 & 1)
        GPIO.output(ALE, GPIO.HIGH)
        GPIO.output(WE,  GPIO.HIGH)
        GPIO.output(WE,  GPIO.LOW)
        GPIO.output(ALE, GPIO.LOW)


def start(mode, red, green):
    #GPIO.cleanup()
    #GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    channels = [SE,AB,A3,A2,A1,A0,DG,CLK,WE,DR,ALE]
    GPIO.setup(channels,GPIO.OUT)
    GPIO.output(SE,  GPIO.LOW)
    GPIO.output(AB,  GPIO.LOW)
    GPIO.output(CLK, GPIO.LOW)
    GPIO.output(ALE, GPIO.LOW)
    GPIO.output(WE,  GPIO.LOW)
    
    if mode == const.DISPLAY_MODE_H:
        showH(red, green)
    else:
        showV(red, green)
        
    GPIO.cleanup()
