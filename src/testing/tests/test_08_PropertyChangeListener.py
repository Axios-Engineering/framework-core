#
# This file is protected by Copyright. Please refer to the COPYRIGHT file
# distributed with this source distribution.
#
# This file is part of REDHAWK core.
#
# REDHAWK core is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# REDHAWK core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

import unittest, os, signal, time
from _unitTestHelpers import scatest
from omniORB import URI, any
from ossie.cf import CF, CF__POA
import CosNaming
import threading
import commands
import ossie.properties as properties
import CosEventComm,CosEventComm__POA
import CosEventChannelAdmin, CosEventChannelAdmin__POA
from ossie.cf import StandardEvent
from ossie.events import ChannelManager
from ossie.utils import redhawk

class PropertyChangeListener_Receiver(CF__POA.PropertyChangeListener):
    def __init__(self):
        self.count = 0

    def propertyChange( self, pce ) :
        self.count = self.count +1


class PropertyChangeListenerTest(scatest.CorbaTestCase):
    def setUp(self):
        self._domBooter, self._domMgr = self.launchDomainManager()

    def tearDown(self):
        try:
            self._app.stop()
            self._app.releaseObject()
        except AttributeError:
            pass

        try:
            self._devMgr.shutdown()
        except AttributeError:
            pass

        try:
            self.terminateChild(self._devBooter)
        except AttributeError:
            pass

        try:
            self.terminateChild(self._domBooter)
        except AttributeError:
            pass

        # Do all application and node booter shutdown before calling the base
        # class tearDown, or failures will occur.
        scatest.CorbaTestCase.tearDown(self)

    def test_PropertyChangeListener_CPP(self):
        self.localEvent = threading.Event()
        self.eventFlag = False

        self._devBooter, self._devMgr = self.launchDeviceManager("/nodes/test_BasicTestDevice_node/DeviceManager.dcd.xml", self._domMgr)
        self.assertNotEqual(self._devBooter, None)
        self._domMgr.installApplication("/waveforms/PropertyChangeListener/PropertyChangeListener.sad.xml")
        appFact = self._domMgr._get_applicationFactories()[0]
        self.assertNotEqual(appFact, None)
        app = appFact.create(appFact._get_name(), [], [])
        self.assertNotEqual(app, None)
        app.start()
        time.sleep(1)

        ps=None
        c=None
        d=redhawk.attach(scatest.getTestDomainName())
        a=d.apps[0]
        c=filter( lambda c : c.name == 'PropertyChange_C1', a.comps )[0]
        self.assertNotEqual(c,None)
        ps = c.ref._narrow(CF.PropertySet)
        self.assertNotEqual(ps,None)
        
        # create listener interface
        myl = PropertyChangeListener_Receiver()
        t=float(0.5)
        regid=ps.registerPropertyListener( myl._this(), ['prop1'],t)

        # assign 3 changed values
        c.prop1 = 100.0
        time.sleep(.6)   # wait for listener to receive notice
        c.prop1 = 200.0
        time.sleep(.6)   # wait for listener to receive notice
        c.prop1 = 300.0
        time.sleep(.6)   # wait for listener to receive notice
        
        # now check results
        self.assertEquals(myl.count,3)

        # change unmonitored property
        c.prop2 = 100
        time.sleep(.6)   # wait for listener to receive notice

        # now check results
        self.assertEquals(myl.count,3)

        # unregister
        ps.unregisterPropertyListener( regid )

        c.prop1 = 100.0
        time.sleep(.6)   # wait for listener to receive notice
        
        # now check results, should be same... 
        self.assertEquals(myl.count,3)

        self.assertRaises( CF.InvalidIdentifier,
            ps.unregisterPropertyListener, regid )
                           

        app.releaseObject()


    def test_PropertyChangeListener_PYTHON(self):
        self.localEvent = threading.Event()
        self.eventFlag = False

        self._devBooter, self._devMgr = self.launchDeviceManager("/nodes/test_BasicTestDevice_node/DeviceManager.dcd.xml", self._domMgr)
        self.assertNotEqual(self._devBooter, None)
        self._domMgr.installApplication("/waveforms/PropertyChangeListener/PropertyChangeListener.sad.xml")
        appFact = self._domMgr._get_applicationFactories()[0]
        self.assertNotEqual(appFact, None)
        app = appFact.create(appFact._get_name(), [], [])
        self.assertNotEqual(app, None)
        app.start()
        time.sleep(1)

        ps=None
        c=None
        d=redhawk.attach(scatest.getTestDomainName())
        a=d.apps[0]
        c=filter( lambda c : c.name == 'PropertyChange_P1', a.comps )[0]
        self.assertNotEqual(c,None)
        ps = c.ref._narrow(CF.PropertySet)
        self.assertNotEqual(ps,None)
        
        # create listener interface
        myl = PropertyChangeListener_Receiver()
        t=float(0.5)
        regid=ps.registerPropertyListener( myl._this(), ['prop1'],t)

        # assign 3 changed values
        c.prop1 = 100.0
        time.sleep(.6)   # wait for listener to receive notice
        c.prop1 = 200.0
        time.sleep(.6)   # wait for listener to receive notice
        c.prop1 = 300.0
        time.sleep(.6)   # wait for listener to receive notice
        
        # now check results
        self.assertEquals(myl.count,3)

        # change unmonitored property
        c.prop2 = 100
        time.sleep(.6)   # wait for listener to receive notice

        # now check results
        self.assertEquals(myl.count,3)

        # unregister
        ps.unregisterPropertyListener( regid )

        c.prop1 = 100.0
        time.sleep(.6)   # wait for listener to receive notice
        
        # now check results, should be same... 
        self.assertEquals(myl.count,3)

        self.assertRaises( CF.InvalidIdentifier,
            ps.unregisterPropertyListener, regid )
                           

        app.releaseObject()



    def test_PropertyChangeListener_JAVA(self):
        self.localEvent = threading.Event()
        self.eventFlag = False

        self._devBooter, self._devMgr = self.launchDeviceManager("/nodes/test_BasicTestDevice_node/DeviceManager.dcd.xml", self._domMgr)
        self.assertNotEqual(self._devBooter, None)
        self._domMgr.installApplication("/waveforms/PropertyChangeListener/PropertyChangeListener.sad.xml")
        appFact = self._domMgr._get_applicationFactories()[0]
        self.assertNotEqual(appFact, None)
        app = appFact.create(appFact._get_name(), [], [])
        self.assertNotEqual(app, None)
        app.start()
        time.sleep(1)

        ps=None
        c=None
        d=redhawk.attach(scatest.getTestDomainName())
        a=d.apps[0]
        c=filter( lambda c : c.name == 'PropertyChange_J1', a.comps )[0]
        self.assertNotEqual(c,None)
        ps = c.ref._narrow(CF.PropertySet)
        self.assertNotEqual(ps,None)
        
        # create listener interface
        myl = PropertyChangeListener_Receiver()
        t=float(0.5)
        regid=ps.registerPropertyListener( myl._this(), ['prop1'],t)

        # assign 3 changed values
        c.prop1 = 100.0
        time.sleep(.6)   # wait for listener to receive notice
        c.prop1 = 200.0
        time.sleep(.6)   # wait for listener to receive notice
        c.prop1 = 300.0
        time.sleep(.6)   # wait for listener to receive notice
        
        # now check results
        self.assertEquals(myl.count,3)

        # change unmonitored property
        c.prop2 = 100
        time.sleep(.6)   # wait for listener to receive notice

        # now check results
        self.assertEquals(myl.count,3)

        # unregister
        ps.unregisterPropertyListener( regid )

        c.prop1 = 100.0
        time.sleep(.6)   # wait for listener to receive notice
        
        # now check results, should be same... 
        self.assertEquals(myl.count,3)

        self.assertRaises( CF.InvalidIdentifier,
            ps.unregisterPropertyListener, regid )
                           

        app.releaseObject()

