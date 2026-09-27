#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
'''
runner.py
17/May/2018
'''
import font
import utils
import spider
from datetime import datetime
import const
from contextlib import closing
import sqlite3
import threading
import time
import os

FONT = font.Font()
dbname = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../db.sqlite3')

def to16(barry):
    result = ''
    st = ''
    while barry:
        st += str(barry.pop(0))
        if len(st) == 4:
            result += format(int(st, 2), 'x')
            st = ''
    return result

def main():
    print(dbname)
    while True:
        messages = spider.getMessages()
        while messages:
            message = messages.pop(0)
            if const.DISPLAY_MODE_H == message['mode']:
                rbytearray, gbytearray = utils.doHorizontal(message['colour'], message['content'], FONT.fonts[message['font']])
            else:
                rbytearray, gbytearray = utils.doVertical(message['colour'], message['content'], FONT.fonts[message['font']])
            size_int = len(rbytearray)
            save(message['title'], message['mode'], to16(gbytearray), to16(rbytearray), size_int, datetime.now())
        time.sleep(5)
            
def save(title_text, mode_int, green_text, red_text, size_int, pub_date):
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM spider_message WHERE title_text = '%s'" % title_text)
        if c.fetchone():
            sql = 'UPDATE spider_message SET mode_int=?, green_text=?, red_text=?, size_int=?, pub_date=? WHERE title_text=?'
            c.execute(sql, (mode_int, green_text, red_text, size_int, pub_date, title_text))
        else:
            sql = 'insert into spider_message(title_text, mode_int, green_text, red_text, size_int, pub_date) values(?,?,?,?,?,?)'
            c.execute(sql, (title_text, mode_int, green_text, red_text, size_int, pub_date))
        conn.commit()
    return (title_text, mode_int, green_text, red_text, size_int, pub_date)

if __name__ == '__main__':
    threading.Thread(target=main).start()

