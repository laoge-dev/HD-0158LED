#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-
'''
sender.py
17/May/2018
'''
import socket
import logging
import time
import threading
import font
import utils
import spider
import datetime
import const

FONT = font.Font()

READY = False
FEEDBACK = True
BEEM = None
logging.basicConfig(filename='sender.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(name)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def doTCP():
    global READY
    global FEEDBACK
    global BEEM
    while True:
        try:
            if READY and FEEDBACK:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((const.TCP_HOST, const.TCP_PORT))
                    data = BEEM.pop(0)
                    BEEM.append(data)
                    s.sendall(bytes(data))
                FEEDBACK = False
        except Exception as e:
            logging.getLogger('sender.py').error("Can't connect to server (%s)", e)
            # sleep 5 seconds
            time.sleep(5)

def doUDP():
    global FEEDBACK
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((const.HOST4BIND, const.UDP_PORT))
        while True:
            data, addr = s.recvfrom(2)
            logging.getLogger('sender.py').debug('Accepting a Connection from (%s)', addr)
            if data == b'OK':
                FEEDBACK = True

def getfeedback():
    doUDP()

def sendtoclient():
    doTCP()

def getmessages():
    global READY
    global BEEM
    while True:
        data = []
        modes, messages, colors, fonts = spider.getMessages()
        while modes:
            if const.DISPLAY_MODE_H == modes.pop():
                data.append(utils.doHorizontal(colors.pop(), messages.pop(), FONT.fonts[fonts.pop()]))
            else:
                data.append(utils.doVertical(colors.pop(), messages.pop(), FONT.fonts[fonts.pop()]))
        READY = False
        BEEM = data
        READY = True
        time.sleep(const.MESSAGE_UPDATE_TIME)

def main():
    threading.Thread(target=getmessages).start()
    threading.Thread(target=sendtoclient).start()
    threading.Thread(target=getfeedback).start()

if __name__ == '__main__':
    main()