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

INCLUDES = -I../include

lib_LTLIBRARIES = libossiecf.la
libossiecf_la_SOURCES = AggregateDevice_impl.cpp \
                        ApplicationFactory_impl.cpp \
                        File_impl.cpp \
                        Application_impl.cpp \
                        FileManager_impl.cpp \
                        PortSupplier_impl.cpp \
                        Device_impl.cpp \
                        FileSystem_impl.cpp \
                        PropertySet_impl.cpp \
                        DeviceManager_impl.cpp \
                        LifeCycle_impl.cpp \
                        Resource_impl.cpp \
                        DomainManager_impl.cpp \
                        ExecutableDevice_impl.cpp \
                        LoadableDevice_impl.cpp \
                        TestableObject_impl.cpp \
                        applicationSupport.cpp \
                        helperFunctions.cpp \
                        Port_impl.cpp \
                        connectionSupport.cpp \
                        FileStream.cpp \
                        POACreator.cpp \
                        CorbaUtils.cpp \
                        ORB.cpp \
                        prop_helpers.cpp \
                        MessageInterface.cpp

if ENABLE_EVENTS
libossiecf_la_SOURCES += DomainManager_Channels.cpp \
			 EventChannelSupport.cpp
endif

libossiecf_la_CXXFLAGS = -Wall $(BOOST_CPPFLAGS) $(OMNICOS_CFLAGS) $(OMNIORB_CFLAGS) $(LOG4CXX_FLAGS) $(PERSISTENCE_CFLAGS)
libossiecf_la_LIBADD = $(BOOST_LDFLAGS) $(BOOST_FILESYSTEM_LIB) $(BOOST_SERIALIZATION_LIB) $(BOOST_REGEX_LIB) $(BOOST_LIBS) $(OMNICOS_LIBS) $(OMNIORB_LIBS) $(LOG4CXX_LIBS) $(PERSISTENCE_LIBS)
libossiecf_la_LDFLAGS = -Wall -version-info $(LIBOSSIECF_VERSION_INFO)

