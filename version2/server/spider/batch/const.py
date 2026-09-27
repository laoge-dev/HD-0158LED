# -*- coding: utf-8 -*-

'''
const.py

16/May/2018
'''
SCREENWIDTH  = 32*4
SCREENHEIGHT = 16

HIGH = '1'
LOW  = '0'

SPACE = LOW + LOW + LOW + LOW

LINE_FEED = '$LF$'

DISPLAY_MODE_V=1
DISPLAY_MODE_H=2

# 10 minutes
MESSAGE_UPDATE_TIME=60*10

SLEEPTIME_MODE_V=0.05
SLEEPTIME_MODE_H=0

FONT_BIG_NORMAL='b16'
FONT_MIDDLE_NORMAL='b14'
FONT_SMALL_NORMAL='b12'
COLOR_RED=1
COLOR_GREEN=2
COLOR_ORANGE=3

# Raspberry pi's IP
TCP_HOST = '192.168.100.106'
TCP_PORT = 20007 # Arbitrary non-privileged port
BUFF_SIZE = 4096 # 4 KiB

# server's IP
UDP_HOST = '192.168.100.250'
UDP_PORT = 40007 # Arbitrary non-privileged port

HOST4BIND = '' # Symbolic name meaning all available interfaces

