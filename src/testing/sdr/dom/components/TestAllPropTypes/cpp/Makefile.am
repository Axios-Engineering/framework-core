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

AM_CXXFLAGS = -Wall $(OMNIORB_CFLAGS) $(OMNITHREAD_CFLAGS) $(OMNIDYNAMIC_CFLAGS) $(BOOST_CPPFLAGS)
AM_LDFLAGS =  -no-install -Wall $(BOOST_LIBS) $(OMNIORB_LIBS) $(OMNITHREAD_LIBS) $(OMNIDYNAMIC_LIBS)
INCLUDES = -I../../../../../../base/include -I../../../../../../base/parser

noinst_PROGRAMS = TestAllPropTypes

#ossieName = TestAllPropTypes
#bindir = $(prefix)/dom/components/TestAllPropTypes/cpp/
#bin_PROGRAMS = TestAllPropTypes

#xmldir = $(prefix)/dom/components/TestAllPropTypes/
#dist_xml_DATA = ../TestAllPropTypes.prf.xml ../TestAllPropTypes.scd.xml ../TestAllPropTypes.spd.xml

distclean-local:
	rm -f config.*
	rm -rf autom4te.cache
	rm -f acinclude.m4
	rm -f aclocal.m4
	rm -f configure
	rm -f depcomp
	rm -f install-sh
	rm -f ltmain.sh
	rm -f Makefile.in
	rm -f missing
	rm -rf .deps

# Sources, libraries and library directories are auto-included from a file
# generated by the REDHAWK IDE. You can remove/modify the following lines if
# you wish to manually control these options.
TestAllPropTypes_SOURCES = main.cpp port_impl.cpp TestAllPropTypes_base.cpp TestAllPropTypes.cpp port_impl.h struct_props.h TestAllPropTypes_base.h TestAllPropTypes.h
TestAllPropTypes_LDADD = $(BOOST_LIBS) ../../../../../../base/framework/libossiecf.la ../../../../../../base/parser/libossieparser.la ../../../../../../base/framework/idl/libossieidl.la $(BOOST_FILESYSTEM_LIB) $(BOOST_REGEX_LIB) $(BOOST_THREAD_LIB) -lboost_serialization
