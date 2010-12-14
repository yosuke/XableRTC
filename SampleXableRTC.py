#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sample of self-extensible RT-component
#           copyright 2010 Yosuke Matsusaka, AIST.

import sys
import locale
import codecs
from pprint import pprint

import OpenRTM_aist
import RTC
from XableRTC import *

SampleXableRTC_spec = ["implementation_id", "SampleXableRTC",
                       "type_name",         "SampleXableRTC",
                       "description",       "Sample self-extensible RT-component",
                       "version",           "1.0.0",
                       "vendor",            "AIST",
                       "category",          "communication",
                       "activity_type",     "DataFlowComponent",
                       "max_instance",      "10",
                       "language",          "Python",
                       "lang_type",         "script",
                       ""]

class SampleXableRTC(XableRTC):
    def onData(self, info, data):
        pprint(info)
        pprint(data)
        print ""

class SampleXableRTCManager:
    def __init__(self):
        self._comp = None
        self._manager = OpenRTM_aist.Manager.init(sys.argv)
        self._manager.setModuleInitProc(self.moduleInit)
        self._manager.activateManager()

    def start(self):
        self._manager.runManager(False)

    def moduleInit(self, manager):
        profile=OpenRTM_aist.Properties(defaults_str=SampleXableRTC_spec)
        manager.registerFactory(profile, SampleXableRTC, OpenRTM_aist.Delete)
        self._comp = manager.createComponent('SampleXableRTC')

def main():
    locale.setlocale(locale.LC_CTYPE, '')
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = 'us-ascii'
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = 'replace')
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = 'replace')
    manager = SampleXableRTCManager()
    manager.start()

if __name__=='__main__':
    main()
