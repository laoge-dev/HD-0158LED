#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
receiver.py

16/May/2018
'''
import socket
import threading
import logging
import time
import wireman
import const

logging.basicConfig(filename='receiver.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(name)s: %(message)s')

BEEM = None
READY = True

def doTCP():
    global BEEM
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((const.HOST4BIND, const.TCP_PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            READY = False
            with conn:
                logging.getLogger('receiver.py').info('Connected by (%s)', addr)
                b = b''
                while True:
                    data = conn.recv(const.BUFF_SIZE)
                    b += data
                    if not data: break
                if b:
                    BEEM = list(b)
                    processing()

def doUDP():
    global READY
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while True:
                if READY:
                    s.sendto(b'OK', (const.UDP_HOST, const.UDP_PORT))
                time.sleep(2)
    except Exception as e:
        logging.getLogger('receiver.py').error("Can't connect to server (%s)", e)
        # sleep 5 seconds
        time.sleep(5)

def sendfeedback():
    doUDP()

def processing():
    global READY
    global BEEM
    if BEEM:
        red = []
        green = []
        dismode = BEEM.pop(0)
        while BEEM:
            red.append(BEEM.pop(0))
            green.insert(0, BEEM.pop())
            
        wireman.start(dismode, red, green)
        READY = True
        BEEM = None

def receiving():
    doTCP()

def main():
    threading.Thread(target=receiving).start()
    threading.Thread(target=sendfeedback).start()

if __name__ == '__main__':
    main()
