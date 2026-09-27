# -*- coding: utf-8 -*-

'''
utils.py

16/May/2018
'''
import const

def BLANK(w=const.SCREENWIDTH, h=const.SCREENHEIGHT):
    return [addplaceholders(w) for _ in range(h)]

def addplaceholders(num):
    result = ''
    while num > 0:
        result += const.LOW
        num-=1
    return result

def todots(aline):
    abyte = int(aline, 16)
    result = ''
    for i in range(len(aline)*4):
        if abyte >> abs(i - len(aline)*4 + 1) & 1:
            result += const.HIGH
        else:
            result += const.LOW
    return result

def todotslist(hexstrlist):
    dotslist = []
    for aline in hexstrlist:
        dotslist.append(todots(aline))
    return dotslist

def trimword(dotslist):
    lflg = False
    rflg = False
    while dotslist[0]:
        for j in range(len(dotslist)):
            if dotslist[j][:1] == const.HIGH:
                lflg = True
            if dotslist[j][-1:] == const.HIGH:
                rflg = True
        for k in range(len(dotslist)):
            if not lflg:
                dotslist[k] = dotslist[k][1:]
            if not rflg:
                dotslist[k] = dotslist[k][:-1]
        if lflg and rflg:
            break

def contact(arr1, arr2):
    for i in range(len(arr1)):
        arr1[i] += arr2[i]

def doHorizontal(color, ptxt, dic):
    
    rbytearray = []
    gbytearray = []
    redlist = BLANK()
    greenlist = BLANK()
    
    for txt in ptxt:
        if txt == const.LINE_FEED:
            contact(redlist, BLANK())
            contact(greenlist, BLANK())
            continue
        c = color.pop(0)
        color.append(c)
        dotmatrix = []
        for aword in txt:
            hexstr = dic[ord(aword)]
            hexstrlist = hexstr.split(',')
            dotslist = todotslist(hexstrlist)
            trimword(dotslist)
            index = 0
            for aline in dotslist:
                if len(dotmatrix) == index:
                    dotmatrix.append('')
                if dotmatrix[index]:
                    dotmatrix[index] += const.LOW
                dotmatrix[index] += aline if aline else const.SPACE
                index += 1

        blankline = addplaceholders(len(dotmatrix[0]))
        insertorappend = False
        while len(dotmatrix) < const.SCREENHEIGHT:
            insertorappend = not insertorappend

            if insertorappend:
                dotmatrix.insert(0, blankline)
            else:
                dotmatrix.append(blankline)
                
        if c & 1:
            contact(redlist, dotmatrix)
        else:
            contact(redlist, BLANK(len(dotmatrix[0])))
        if c >> 1 & 1:
            contact(greenlist, dotmatrix)
        else:
            contact(greenlist, BLANK(len(dotmatrix[0])))

    contact(redlist, BLANK())
    contact(greenlist, BLANK())
        
    for line in redlist:
        for w in line:
            rbytearray.append(int(w))
    for line in greenlist:
        for w in line:
            gbytearray.append(int(w))
            
    return (rbytearray, gbytearray)

def islengthover(dotmatrix, pointline, dotslist):
    result = False

    width = len(dotslist[0])

    if not dotslist[0]:
        width = len(const.SPACE)

    if len(dotmatrix) > pointline * len(dotslist):
        gap = len(dotmatrix[len(dotmatrix) - 1]) + width - const.SCREENWIDTH
        if gap > 0:
            result = True

    if not dotslist[0]:
        for i in range(len(dotslist)):
            if result:
                dotslist[i] = addplaceholders(gap)
            else:
                dotslist[i] = const.SPACE

    return result

def clearblankrows(a, r, g):
    isblankpreline = False
    for i in reversed(range(len(a))):
        isblankline = True
        for j in a[i]:
            if j == const.HIGH:
                isblankline = False
        if isblankline:
            if isblankpreline or i == len(a)-1:
                del a[i]
                del r[i]
                del g[i]
            else:
                isblankpreline = True
        else:
            isblankpreline = False

    topline = a.pop(0)
    for k in topline:
        if k == const.HIGH:
            a.insert(0, topline)
            break

def fill(dotmatrix):
    for i in range(len(dotmatrix)):
        dotmatrix[i] += addplaceholders(const.SCREENWIDTH - len(dotmatrix[i]))
        
    blankline = addplaceholders(const.SCREENWIDTH)
    for _ in range(const.SCREENHEIGHT):
        dotmatrix.insert(0, blankline)
        dotmatrix.append(blankline)

def doVertical(color, ptxt, dic):
    
    rbytearray = []
    gbytearray = []
    redlist = []
    greenlist = []
    dotmatrix = []
    pointline = 0
    for txt in ptxt:
        if txt == const.LINE_FEED:
            pointline += 1
            continue
        c = color.pop(0)
        color.append(c)
        for aword in txt:
            hexstr = dic[ord(aword)]
            hexstrlist = hexstr.split(',')
            dotslist = todotslist(hexstrlist)
            trimword(dotslist)
            if islengthover(dotmatrix, pointline, dotslist):
                pointline += 1

            index = pointline * len(dotslist)
            for aline in dotslist:
                if len(dotmatrix) == index:
                    dotmatrix.append('')
                    redlist.append('')
                    greenlist.append('')
                dotmatrix[index] += aline
                
                if c & 1:
                    redlist[index] += aline
                else:
                    redlist[index] += addplaceholders(len(aline))
                if c >> 1 & 1:
                    greenlist[index] += aline
                else:
                    greenlist[index] += addplaceholders(len(aline))

                if len(dotmatrix[index]) < const.SCREENWIDTH:
                    dotmatrix[index] += const.LOW
                    redlist[index] += const.LOW
                    greenlist[index] += const.LOW
                index += 1

    clearblankrows(dotmatrix, redlist, greenlist)
    fill(redlist)
    fill(greenlist)
    
    for line in redlist:
        for w in line:
            rbytearray.append(int(w))
    for line in greenlist:
        for w in line:
            gbytearray.append(int(w))
            
    return (rbytearray, gbytearray)

