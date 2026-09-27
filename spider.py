# -*- coding: utf-8 -*-

'''
spider.py
17/May/2018
'''
import const
import datetime

import requests
from bs4 import BeautifulSoup

def getWeather():
    soup  = BeautifulSoup(requests.get('https://weather.yahoo.co.jp/weather/jp/12/4510.html').content, "lxml")
    date = soup.select('p.date')
    pict = soup.select('p.pict')
    thigh = soup.select('li.high')
    tlow = soup.select('li.low')
    Weather = [date[0].text + ' ', pict[0].text + ' ', thigh[0].text + ' ', tlow[0].text + '  ', date[1].text + ' ', pict[1].text + ' ', thigh[1].text + ' ', tlow[1].text]
    return Weather

def getTrumpTwitter():
    soup  = BeautifulSoup(requests.get('https://twitter.com/realDonaldTrump').content, "lxml")
    TrumpT = [soup.select_one("div.js-tweet-text-container p").text, const.LINE_FEED, soup.title.text.split('(')[0]]
    return TrumpT

def getStocks():
    soup  = BeautifulSoup(requests.get('https://stocks.finance.yahoo.co.jp/').content, "lxml")

    title = soup.select('td.yjSt dt.DataTitle a')
    fl = soup.select('td.yjSt dd.pad4 strong.floatL')
    fr = soup.select('td.yjSt dd.pad4 span.floatR ')
    
    
    text = []
    colour = []
    for _ in range(3):
        title = title.pop(0).text
        fltext = fl.pop(0).text
        frtext = fr.pop(0).text
        text.append(title + ' ')
        colour.append(const.COLOR_ORANGE)
        text.append(fltext + ' ' + frtext)
        if fltext.startswith('-'):
            colour.append(const.COLOR_RED)
        else:
            colour.append(const.COLOR_GREEN)
    return (text, colour)

def getMessages():
    modes = []
    messages = []
    colors = []
    fonts = []
    
    modes.append(const.DISPLAY_MODE_H)
    messages.append(getWeather())
    colors.append([3,2,1,2])
    fonts.append(const.FONT_MIDDLE_NORMAL)
    
    modes.append(const.DISPLAY_MODE_V)
    messages.append(getTrumpTwitter())
    colors.append([3,2])
    fonts.append(const.FONT_SMALL_NORMAL)

    modes.append(const.DISPLAY_MODE_H)
    text, colour = getStocks()
    messages.append(text)
    colors.append(colour)
    fonts.append(const.FONT_MIDDLE_NORMAL)
    
    return (modes, messages, colors, fonts)
