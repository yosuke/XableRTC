#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sample pattern generator for testing self-extensible RT-component
#           copyright 2010 Yosuke Matsusaka, AIST.

import sys
import locale
import codecs
from random import randint

import OpenRTM_aist
import RTC

SamplePatternGeneratorRTC_spec = ["implementation_id", "SamplePatternGeneratorRTC",
                                  "type_name",         "SamplePatternGeneratorRTC",
                                  "description",       "Sample pattern generator",
                                  "version",           "1.0.0",
                                  "vendor",            "AIST",
                                  "category",          "communication",
                                  "activity_type",     "DataFlowComponent",
                                  "max_instance",      "10",
                                  "language",          "Python",
                                  "lang_type",         "script",
                                  ""]

class SamplePatternGeneratorRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._intnum = 5
        self._intports = {}
        self._intdata = {}
        self._strport = None
        self._strdata = None

    def onInitialize(self):
        # create outports for random int valiables
        for i in range(self._intnum):
            pname = "intport%s" % (i,)
            data = RTC.TimedLong(RTC.Time(0,0), 0)
            port = OpenRTM_aist.OutPort(pname, data)
            self.addOutPort(pname, port)
            self._intports[pname] = port
            self._intdata[pname] = data
        # create outport for string valiable
        self._strdata = RTC.TimedString(RTC.Time(0,0), "")
        self._strport = OpenRTM_aist.OutPort('strport', self._strdata)
        self.addOutPort(self._strport._name, self._strport)
        return RTC.RTC_OK

    def onExecute(self, ec_id):
        for i in range(self._intnum):
            pname = "intport%s" % (i,)
            self._intdata[pname].data = randint(1, 10)
            self._intports[pname].write(self._intdata[pname])
        if randint(1, 10) > 3:
            self._strdata.data = "normal"
        else:
            self._strdata.data = "emergency"
        self._strport.write(self._strdata)
        return RTC.RTC_OK

class SamplePatternGeneratorRTCManager:
    def __init__(self):
        self._comp = None
        self._manager = OpenRTM_aist.Manager.init(sys.argv)
        self._manager.setModuleInitProc(self.moduleInit)
        self._manager.activateManager()

    def start(self):
        self._manager.runManager(False)

    def moduleInit(self, manager):
        profile=OpenRTM_aist.Properties(defaults_str=SamplePatternGeneratorRTC_spec)
        manager.registerFactory(profile, SamplePatternGeneratorRTC, OpenRTM_aist.Delete)
        self._comp = manager.createComponent('SamplePatternGeneratorRTC?exec_cxt.periodic.rate=1')

def main():
    locale.setlocale(locale.LC_CTYPE, '')
    encoding = locale.getlocale()[1]
    if not encoding:
        encoding = 'us-ascii'
    sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = 'replace')
    sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = 'replace')
    manager = SamplePatternGeneratorRTCManager()
    manager.start()

if __name__=='__main__':
    main()
