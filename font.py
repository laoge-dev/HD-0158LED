# -*- coding: utf-8 -*-

'''
font.py

16/May/2018
'''
import os
import fnmatch
class Font:
    def __init__(self):
        self.fonts = dict()
        for f in os.listdir('.'):
            if fnmatch.fnmatch(f.upper(), '*.BDF'):
                bdf = self.parseBDF(f)
                self.fonts[f[:-4]] = bdf

    def parseBDF(self, f):
        isbegin = False
        ucode = 0
        doc = dict()
        content = ''
        with open(f, 'r') as bdf:
            for line in bdf.readlines():
                if line.startswith('ENDCHAR'):
                    isbegin = False
                    content = content[:-1]
                    doc[ucode] = content
                if isbegin:
                    content += line[:-1] + ','
                if line.startswith('ENCODING'):
                    ucode = int(line[9:])
                if line.startswith('BITMAP'):
                    isbegin = True
                    content = ''
        return doc