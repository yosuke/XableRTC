# -*- coding: utf-8 -*-

# Base class of self-extensible RT-component
#           copyright 2010 Yosuke Matsusaka, AIST.

import OpenRTM_aist
import RTC

class DataListener(OpenRTM_aist.ConnectorDataListenerT):
    '''callback function for data received event'''
    def __init__(self, name, obj, dtype):
        self._name = name
        self._obj = obj
        self._dtype = dtype
    def __call__(self, info, cdrdata):
        data = OpenRTM_aist.ConnectorDataListenerT.__call__(self, info, cdrdata, self._dtype(RTC.Time(0, 0), None))
        self._obj.onData(self._name, data)

class ConnectListener(OpenRTM_aist.ConnectorListener):
    '''callback function for connect event'''
    def __init__(self, name, obj):
        self._name = name
        self._obj = obj
    def __call__(self, info):
        self._obj.onConnect(self._name, info)

class DisConnectListener(OpenRTM_aist.ConnectorListener):
    '''callback function for disconnect event'''
    def __init__(self, name, obj):
        self._name = name
        self._obj = obj
    
    def __call__(self, info):
        self._obj.onDisConnect(self._name, info)

class XableRTC(OpenRTM_aist.DataFlowComponentBase):
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
        self._xinports = {}
        self._xinportcount = 0
        self._xoutports = {}
        self._xoutportcount = 0
        self._xoutporttypes = {}

    def onInitialize(self):
        '''initilization function of self extending RTC'''
        self.addIncreasableInPort()
        self.addIncreasableOutPort()
        return RTC.RTC_OK
    
    def addIncreasableInPort(self):
        '''create inport with connection callback'''
        pname = "inport%i" % (self._xinportcount,)
        port = OpenRTM_aist.InPort(pname, RTC.TimedString(RTC.Time(0,0), ""))
        port.appendProperty("dataport.data_type", "Any")
        port.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_CONNECT,
                                  ConnectListener(pname, self), True)
        self._xinports[pname] = port
        self._xinportcount += 1
        self.addInPort(pname, port)
    
    def addIncreasableOutPort(self):
        '''create outport with connection callback'''
        pname = "outport%i" % (self._xoutportcount,)
        port = OpenRTM_aist.OutPort(pname, RTC.TimedString(RTC.Time(0,0), ""))
        port.appendProperty("dataport.data_type", "Any")
        port.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_CONNECT,
                                  ConnectListener(pname, self), True)
        self._xoutports[pname] = port
        self._xoutportcount += 1
        self._xoutporttypes[pname] = None
        self.addOutPort(pname, port)
    
    def onConnect(self, pname, info):
        '''connect callback'''
        if pname in self._xinports:
            port = self._xinports[pname]
            targetDataType = eval("RTC." + info.properties.getProperty("data_type"))
            port.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,
                                          DataListener(pname, self, targetDataType))
            port.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_DISCONNECT,
                                      DisConnectListener(pname, self), True)
            self.addIncreasableInPort()
        elif pname in self._xoutports:
            port = self._xoutports[pname]
            targetDataType = eval("RTC." + info.properties.getProperty("data_type"))
            self._xoutporttypes[pname] = targetDataType
            port.addConnectorListener(OpenRTM_aist.ConnectorListenerType.ON_DISCONNECT,
                                      DisConnectListener(pname, self), True)
            self.addIncreasableOutPort()

    def onDisConnect(self, pname, info):
        '''disconnect callback'''
        if pname in self._xinports:
            port = self._xinports[pname]
            self.removeInport(port)
        elif pname in self._xoutports:
            port = self._xinports[pname]
            self.removeInport(port)

    def onData(self, pname, data):
        '''data receive callback'''
        pass

