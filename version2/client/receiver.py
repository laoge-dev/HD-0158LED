#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
receiver.py

16/May/2018
'''
import threading
import wireman
import requests
#import json

def processing(data):
    while data:
        msg_obj = data.pop(0)
        mode_int = msg_obj['mode']
        red_array = toBin(msg_obj['r'])
        green_array = toBin(msg_obj['g'])
        wireman.start(mode_int, red_array, green_array)

def toBin(s_data):
    result = []
    for b in s_data:
        for a in format(int(b, 16), '0>4b'):
            result.append(int(a))
    return result

def receiving():
    url = "http://firefrog.mooo.com:7000/spider/"
    headers = {"content-type": "application/json"}
    r = requests.get(url, headers=headers)
    data = r.json()
    #print (json.dumps(data, indent=2))
    return data

def main():
    while True:
        processing(receiving())

if __name__ == '__main__':
    threading.Thread(target=main).start()
    #threading.Thread(target=processing).start()

