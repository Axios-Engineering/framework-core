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

import unittest, os
import scatest
from omniORB import URI, any
from ossie.cf import CF

class ApplicationFactoryTest(scatest.CorbaTestCase):
    def setUp(self):
        domBooter, self._domMgr = self.launchDomainManager(debug=9)
        self._testFiles = []

    def tearDown(self):
        scatest.CorbaTestCase.tearDown(self)
        for file in self._testFiles:
            os.unlink(file)

    def test_cpp_BasicOperation(self):
        self.assertNotEqual(self._domMgr, None)

        self.assertEqual(len(self._domMgr._get_applicationFactories()), 0)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        self._domMgr.installApplication("/waveforms/CommandWrapperOsProcessor/CommandWrapper.sad.xml")
        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        # Ensure the expected device is available
        devBooter, devMgr = self.launchDeviceManager("/nodes/test_ExecutableDevice_node/DeviceManager.dcd.xml", debug=9)
        self.assertNotEqual(devMgr, None)
        self.assertEqual(len(devMgr._get_registeredDevices()), 1)
        device = devMgr._get_registeredDevices()[0]

        appFact = self._domMgr._get_applicationFactories()[0]

        app = appFact.create(appFact._get_name(), [], []) # LOOK MA, NO DAS!

        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 1)

        # Verify that properties have been changed from their defaults
        self.assertEqual(len(app._get_componentNamingContexts()), 1)
        compName = app._get_componentNamingContexts()[0]
        comp = self._root.resolve(URI.stringToName(compName.elementId))._narrow(CF.Resource)
        self.assertNotEqual(comp, None)

        cmd = comp.query([CF.DataType(id="DCE:a4e7b230-1d17-4a86-aeff-ddc6ea3df26e", value=any.to_any(None))])[0]
        args = comp.query([CF.DataType(id="DCE:5d8bfe8d-bc25-4f26-8144-248bc343aa53", value=any.to_any(None))])[0]
        self.assertEqual(cmd.value._v, "/bin/echo")
        self.assertEqual(args.value._v, ["Hello World"])

        app.stop()
        app.releaseObject()
        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        self._domMgr.uninstallApplication(appFact._get_identifier())

    def test_EmptyDir(self):
        self.assertNotEqual(self._domMgr, None)

        self.assertEqual(len(self._domMgr._get_applicationFactories()), 0)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        self._domMgr.installApplication("/waveforms/CommandWrapperEmptyDir/CommandWrapperEmptyDir.sad.xml")
        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        # Ensure the expected device is available
        devBooter, devMgr = self.launchDeviceManager("/nodes/test_BasicTestDevice_node/DeviceManager.dcd.xml", debug=9)
        self.assertNotEqual(devMgr, None)
        self.assertEqual(len(devMgr._get_registeredDevices()), 1)
        device = devMgr._get_registeredDevices()[0]

        appFact = self._domMgr._get_applicationFactories()[0]

        app = appFact.create(appFact._get_name(), [], []) # LOOK MA, NO DAS!

        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 1)

        app.start()
        app.stop()
        fs = devMgr._get_fileSys()
        contents = fs.list('/.BasicTestDevice_node/BasicTestDevice1/components/CommandWrapperEmptyDir/cmd_dir/tmp')
        foundEmptyDirectory = False
        for entry in contents:
            if entry.name == 'tmp':
                foundEmptyDirectory = True
                break
        self.assertEqual(foundEmptyDirectory, True)
        app.releaseObject()
        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        self._domMgr.uninstallApplication(appFact._get_identifier())

    def test_cpp_DirectoryLoad(self):
        self.assertNotEqual(self._domMgr, None)

        # Verify in the devices cache is emtpy
        componentDir = os.path.join(scatest.getSdrPath(), "dom", "components", "CommandWrapperWithDirectoryLoad")
        deviceCacheDir = os.path.join(scatest.getSdrPath(), "dev", ".ExecutableDevice_node", "ExecutableDevice1", "components", "CommandWrapperWithDirectoryLoad")
        if os.path.exists(deviceCacheDir):
            os.system("rm -rf %s" % deviceCacheDir)

        self.assertEqual(len(self._domMgr._get_applicationFactories()), 0)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        self._domMgr.installApplication("/waveforms/CommandWrapperWithDirectoryLoad/CommandWrapper.sad.xml")
        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        # Ensure the expected device is available
        devBooter, devMgr = self.launchDeviceManager("/nodes/test_ExecutableDevice_node/DeviceManager.dcd.xml", debug=9)
        self.assertNotEqual(devMgr, None)
        self.assertEqual(len(devMgr._get_registeredDevices()), 1)
        device = devMgr._get_registeredDevices()[0]

        appFact = self._domMgr._get_applicationFactories()[0]

        app = appFact.create(appFact._get_name(), [], []) # LOOK MA, NO DAS!

        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 1)

        # Verify that properties have been changed from their defaults
        self.assertEqual(len(app._get_componentNamingContexts()), 1)
        compName = app._get_componentNamingContexts()[0]
        comp = self._root.resolve(URI.stringToName(compName.elementId))._narrow(CF.Resource)
        self.assertNotEqual(comp, None)

        cmd = comp.query([CF.DataType(id="DCE:a4e7b230-1d17-4a86-aeff-ddc6ea3df26e", value=any.to_any(None))])[0]
        args = comp.query([CF.DataType(id="DCE:5d8bfe8d-bc25-4f26-8144-248bc343aa53", value=any.to_any(None))])[0]
        self.assertEqual(cmd.value._v, "/bin/echo")
        self.assertEqual(args.value._v, ["Hello World"])

        app.stop()
        app.releaseObject()
        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        self._domMgr.uninstallApplication(appFact._get_identifier())

    def test_py_BasicOperation(self):
        self.assertNotEqual(self._domMgr, None)

        self.assertEqual(len(self._domMgr._get_applicationFactories()), 0)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        self._domMgr.installApplication("/waveforms/CommandWrapperOsProcessor/CommandWrapper.sad.xml")
        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        # Ensure the expected device is available
        devBooter, devMgr = self.launchDeviceManager("/nodes/test_BasicTestDevice_node/DeviceManager.dcd.xml", debug=9)
        self.assertNotEqual(devMgr, None)
        self.assertEqual(len(devMgr._get_registeredDevices()), 1)
        device = devMgr._get_registeredDevices()[0]

        appFact = self._domMgr._get_applicationFactories()[0]

        app = appFact.create(appFact._get_name(), [], []) # LOOK MA, NO DAS!

        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 1)

        # Verify that properties have been changed from their defaults
        self.assertEqual(len(app._get_componentNamingContexts()), 1)
        compName = app._get_componentNamingContexts()[0]
        comp = self._root.resolve(URI.stringToName(compName.elementId))._narrow(CF.Resource)
        self.assertNotEqual(comp, None)

        cmd = comp.query([CF.DataType(id="DCE:a4e7b230-1d17-4a86-aeff-ddc6ea3df26e", value=any.to_any(None))])[0]
        args = comp.query([CF.DataType(id="DCE:5d8bfe8d-bc25-4f26-8144-248bc343aa53", value=any.to_any(None))])[0]
        self.assertEqual(cmd.value._v, "/bin/echo")
        self.assertEqual(args.value._v, ["Hello World"])

        app.stop()
        app.releaseObject()
        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        self._domMgr.uninstallApplication(appFact._get_identifier())

    def test_py_DirectoryLoad(self):
        self.assertNotEqual(self._domMgr, None)

        self.assertEqual(len(self._domMgr._get_applicationFactories()), 0)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        # Verify in the devices cache is emtpy
        componentDir = os.path.join(scatest.getSdrPath(), "dom", "components", "CommandWrapperWithDirectoryLoad")
        deviceCacheDir = os.path.join(scatest.getSdrPath(), "dev", ".BasicTestDevice_node", "BasicTestDevice1", "components", "CommandWrapperWithDirectoryLoad")
        if os.path.exists(deviceCacheDir):
            os.system("rm -rf %s" % deviceCacheDir)

        self._domMgr.installApplication("/waveforms/CommandWrapperWithDirectoryLoad/CommandWrapper.sad.xml")
        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        # Ensure the expected device is available
        devBooter, devMgr = self.launchDeviceManager("/nodes/test_BasicTestDevice_node/DeviceManager.dcd.xml", debug=9)
        self.assertNotEqual(devMgr, None)
        self.assertEqual(len(devMgr._get_registeredDevices()), 1)
        device = devMgr._get_registeredDevices()[0]

        appFact = self._domMgr._get_applicationFactories()[0]

        app = appFact.create(appFact._get_name(), [], []) # LOOK MA, NO DAS!

        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 1)

        # Verify that properties have been changed from their defaults
        self.assertEqual(len(app._get_componentNamingContexts()), 1)
        compName = app._get_componentNamingContexts()[0]
        comp = self._root.resolve(URI.stringToName(compName.elementId))._narrow(CF.Resource)
        self.assertNotEqual(comp, None)

        cmd = comp.query([CF.DataType(id="DCE:a4e7b230-1d17-4a86-aeff-ddc6ea3df26e", value=any.to_any(None))])[0]
        args = comp.query([CF.DataType(id="DCE:5d8bfe8d-bc25-4f26-8144-248bc343aa53", value=any.to_any(None))])[0]
        self.assertEqual(cmd.value._v, "/bin/echo")
        self.assertEqual(args.value._v, ["Hello World"])

        # Verify in the devices cache that the directory structure was mirrored exactly
        for root, dirs, files in os.walk(componentDir):
            # turn the abs path in to a relative path
            rel_root = root[len(componentDir)+1:]
            for dir in dirs:
                # Hidden files aren't loaded
                if dir[0] != ".":
                    expectedDir = os.path.join(deviceCacheDir, rel_root, dir)
                    self.assertEqual(os.path.isdir(expectedDir), True, "Dir %s not found at %s" % (dir, expectedDir))
                else:
                    # Don't descend into hidden sub-dirs
                    dirs.remove(dir)
            for f in files:
                # Hidden files aren't loaded
                if f[0] != ".":
                    expectedFile = os.path.join(deviceCacheDir, rel_root, f)
                    self.assertEqual(os.path.isfile(expectedFile), True, "File %s not found at %s" % (f, expectedFile))

        app.stop()
        app.releaseObject()
        self.assertEqual(len(self._domMgr._get_applicationFactories()), 1)
        self.assertEqual(len(self._domMgr._get_applications()), 0)

        self._domMgr.uninstallApplication(appFact._get_identifier())

    def test_py_UnloadOnRelease(self):
        # Test that releasing the device unloads all files
        deviceCacheDir = os.path.join(scatest.getSdrPath(), "dev", ".BasicTestDevice_node", "BasicTestDevice1")
        if os.path.exists(deviceCacheDir):
            os.system("rm -rf %s" % deviceCacheDir)

        self.assertNotEqual(self._domMgr, None)

        # Ensure the expected device is available
        devBooter, devMgr = self.launchDeviceManager("/nodes/test_BasicTestDevice_node/DeviceManager.dcd.xml", debug=9)
        self.assertNotEqual(devMgr, None)
        self.assertEqual(len(devMgr._get_registeredDevices()), 1)
        device = devMgr._get_registeredDevices()[0]

        self.assert_(not os.path.exists(deviceCacheDir + "/components/CommandWrapper"))
        self.assert_(not os.path.exists(deviceCacheDir + "/components/CapacityUser"))

        # Load a some files and directories
        device.load(self._domMgr._get_fileMgr(), "/components/CommandWrapper", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.py", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.prf.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.scd.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.spd.xml", CF.LoadableDevice.EXECUTABLE)

        # Simply check that the cache dir isn't empty and has the correct number of files
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 4)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 4)

        device.releaseObject()
        
        # Wait for the device to unregister.
        self.assert_(self._waitRegisteredDevices(devMgr, 0))

        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 0)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 0)

        self.assertEqual(len(self._domMgr._get_deviceManagers()), 1)

    def test_py_LoadUnload(self):
        # Test that releasing the device unloads all files
        deviceCacheDir = os.path.join(scatest.getSdrPath(), "dev", ".BasicTestDevice_node", "BasicTestDevice1")
        if os.path.exists(deviceCacheDir):
            os.system("rm -rf %s" % deviceCacheDir)

        self.assertNotEqual(self._domMgr, None)

        # Ensure the expected device is available
        devBooter, devMgr = self.launchDeviceManager("/nodes/test_BasicTestDevice_node/DeviceManager.dcd.xml", debug=9)
        self.assertNotEqual(devMgr, None)
        self.assertEqual(len(devMgr._get_registeredDevices()), 1)
        device = devMgr._get_registeredDevices()[0]

        self.assert_(not os.path.exists(deviceCacheDir + "/components/CommandWrapper"))
        self.assert_(not os.path.exists(deviceCacheDir + "/components/CapacityUser"))

        # Load a some files and directories
        device.load(self._domMgr._get_fileMgr(), "/components/CommandWrapper", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.py", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.prf.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.scd.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.spd.xml", CF.LoadableDevice.EXECUTABLE)

        # Simply check that the cache dir isn't empty and has the correct number of files
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 4)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 4)

        # Check that a second load doesn't do anything weird
        device.load(self._domMgr._get_fileMgr(), "/components/CommandWrapper", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.py", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.prf.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.scd.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.spd.xml", CF.LoadableDevice.EXECUTABLE)

        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 4)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 4)

        # Clear out the deviceCache
        os.system("rm -rf %s" % (deviceCacheDir + "/components/CommandWrapper"))
        os.system("rm -rf %s" % (deviceCacheDir + "/components/CapacityUser/CapacityUser.py"))

        self.assertEqual(os.path.exists(deviceCacheDir + "/components/CommandWrapper"), False)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 3)

        # Load files and directories, this should copy the files over because they don't exist, even if though the refCnt > 0
        device.load(self._domMgr._get_fileMgr(), "/components/CommandWrapper", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.py", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.prf.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.scd.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.spd.xml", CF.LoadableDevice.EXECUTABLE)

        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 4)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 4)

        # Now we need to unload 3 times
        for i in xrange(3):
            self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 4)
            self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 4)

            device.unload("/components/CommandWrapper")
            device.unload("/components/CapacityUser/CapacityUser.py")
            device.unload("/components/CapacityUser/CapacityUser.prf.xml")
            device.unload("/components/CapacityUser/CapacityUser.scd.xml")
            device.unload("/components/CapacityUser/CapacityUser.spd.xml")
        
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 0)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 0)

        device.releaseObject()

        # Wait for the device to unregister.
        self.assert_(self._waitRegisteredDevices(devMgr, 0))

        self.assertEqual(len(self._domMgr._get_deviceManagers()), 1)

    def test_cpp_LoadUnload(self):
        # Test that releasing the device unloads all files
        deviceCacheDir = os.path.join(scatest.getSdrPath(), "dev", ".ExecutableDevice_node", "ExecutableDevice1")
        if os.path.exists(deviceCacheDir):
            os.system("rm -rf %s" % deviceCacheDir)

        self.assertNotEqual(self._domMgr, None)

        # Ensure the expected device is available
        devBooter, devMgr = self.launchDeviceManager("/nodes/test_ExecutableDevice_node/DeviceManager.dcd.xml", debug=9)
        self.assertNotEqual(devMgr, None)
        self.assertEqual(len(devMgr._get_registeredDevices()), 1)
        device = devMgr._get_registeredDevices()[0]

        self.assert_(not os.path.exists(deviceCacheDir + "/components/CommandWrapper"))
        self.assert_(not os.path.exists(deviceCacheDir + "/components/CapacityUser"))

        # Load a some files and directories
        device.load(self._domMgr._get_fileMgr(), "/components/CommandWrapper", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.py", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.prf.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.scd.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.spd.xml", CF.LoadableDevice.EXECUTABLE)

        # Simply check that the cache dir isn't empty and has the correct number of files
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 4)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 4)

        # Check that a second load doesn't do anything weird
        device.load(self._domMgr._get_fileMgr(), "/components/CommandWrapper", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.py", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.prf.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.scd.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.spd.xml", CF.LoadableDevice.EXECUTABLE)

        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 4)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 4)

        # Clear out the deviceCache
        os.system("rm -rf %s" % (deviceCacheDir + "/components/CommandWrapper"))
        os.system("rm -rf %s" % (deviceCacheDir + "/components/CapacityUser/CapacityUser.py"))

        self.assertEqual(os.path.exists(deviceCacheDir + "/components/CommandWrapper"), False)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 3)

        # Load files and directories, this should copy the files over because they don't exist, even if though the refCnt > 0
        device.load(self._domMgr._get_fileMgr(), "/components/CommandWrapper", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.py", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.prf.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.scd.xml", CF.LoadableDevice.EXECUTABLE)
        device.load(self._domMgr._get_fileMgr(), "/components/CapacityUser/CapacityUser.spd.xml", CF.LoadableDevice.EXECUTABLE)

        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 4)
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 4)

        # Now we need to unload 3 times
        print os.listdir(deviceCacheDir + "/components")
        for i in xrange(3):
            self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 4)
            self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 4)

            device.unload("/components/CommandWrapper")
            device.unload("/components/CapacityUser/CapacityUser.py")
            device.unload("/components/CapacityUser/CapacityUser.prf.xml")
            device.unload("/components/CapacityUser/CapacityUser.scd.xml")
            device.unload("/components/CapacityUser/CapacityUser.spd.xml")


        #self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CommandWrapper")), 0)
        # Empty directories get deleted
        self.assert_(not os.path.exists(deviceCacheDir + "/components/CommandWrapper"))
        self.assertEqual(len(os.listdir(deviceCacheDir + "/components/CapacityUser")), 0)

        device.releaseObject()

        # Wait for the device to unregister.
        self.assert_(self._waitRegisteredDevices(devMgr, 0))

        self.assertEqual(len(self._domMgr._get_deviceManagers()), 1)

    def _test_FileChanged(self, nodeName, deviceName):
        # Test that updating a file in the SCA filesystem causes a device to reload that file
        # in its cache.
        deviceCacheDir = os.path.join(scatest.getSdrPath(), "dev", "." + nodeName, deviceName)
        if os.path.exists(deviceCacheDir):
            os.system("rm -rf %s" % deviceCacheDir)

        self.assertNotEqual(self._domMgr, None)
        fileMgr = self._domMgr._get_fileMgr()
        
        # Ensure the expected device is available
        devBooter, devMgr = self.launchDeviceManager(dcdFile="/nodes/test_%s/DeviceManager.dcd.xml" % nodeName, debug=9)
        self.assertNotEqual(devMgr, None)
        self.assertEqual(len(devMgr._get_registeredDevices()), 1)
        device = devMgr._get_registeredDevices()[0]

        # Create the initial file we'll be loading.
        testFile = 'test.out'
        scaPath = '/' + testFile
        srcFile = os.path.join(os.environ['SDRROOT'], 'dom', testFile)
        f = open(srcFile, 'w')
        f.write('Pre')
        f.close()
        self._testFiles.append(srcFile)

        # Load the initial file onto the device and verify that it contains the expected text.
        device.load(fileMgr, scaPath, CF.LoadableDevice.EXECUTABLE)
        cacheFile = os.path.join(deviceCacheDir, testFile)
        f = open(cacheFile, 'r')
        self.assertEqual(f.readline(), 'Pre')
        f.close()

        # Update the file, making sure that the modification time is more recent than the cached file.
        f = open(srcFile, 'w')
        f.write('Post')
        f.close()
        os.utime(srcFile, (os.path.getatime(cacheFile), os.path.getmtime(cacheFile)+1))

        # Load the file again and verify that the cache has been updated.
        device.load(fileMgr, scaPath, CF.LoadableDevice.EXECUTABLE)
        f = open(cacheFile, 'r')
        self.assertEqual(f.readline(), 'Post')
        f.close()

    def test_DeviceBadLoadable(self):
        devBooter, devMgr = self.launchDeviceManager("/nodes/SimpleDevMgr/DeviceManager.dcd.xml", debug=9)
        device = devMgr._get_registeredDevices()[0]
        fileSys = devMgr._get_fileSys()
        self.assertRaises(CF.LoadableDevice.InvalidLoadKind, device.load, fileSys, '/nodes/SimpleDevMgr/DeviceManager.dcd.xml',CF.LoadableDevice.DRIVER)

    def test_cpp_FileChanged(self):
        self._test_FileChanged("ExecutableDevice_node", "ExecutableDevice1")

    def test_py_FileChanged(self):
        self._test_FileChanged("BasicTestDevice_node", "BasicTestDevice1")

if __name__ == "__main__":
  # Run the unittests
  unittest.main()
