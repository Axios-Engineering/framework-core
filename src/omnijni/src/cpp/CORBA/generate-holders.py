#!/usr/bin/python
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

import sys
from omniidl import idlast, idltype
from omnijni import cppcode
from omnijni import idljni

holderTypes = (
    idltype.tk_boolean,
    idltype.tk_octet,
    idltype.tk_char,
    idltype.tk_short,
    idltype.tk_ushort,
    idltype.tk_long,
    idltype.tk_ulong,
    idltype.tk_longlong,
    idltype.tk_ulonglong,
    idltype.tk_float,
    idltype.tk_double,
    idltype.tk_any
    )

class HolderType(idltype.Type):
    def __init__(self, kind):
        idltype.Type.__init__(self, kind, False)

    def identifier(self):
        return self.scopedName()[-1]

    def scopedName(self):
        return idljni.typeString(self.aliasType()).split('::')

    def aliasType(self):
        return idltype.Base(self.kind())

if __name__ == '__main__':
    header = cppcode.Header('holders.h')
    header.include('<omniORB4/CORBA.h>')
    header.include('<jni.h>')
    body = header.Namespace('CORBA').Namespace('jni')

    module = cppcode.Module()
    module.include('<omnijni/class.h>')
    module.include('<omnijni/any.h>')
    module.include('"holders.h"')

    helper = idljni.HolderHelper()
    for kind in holderTypes:
        # Create a fake IDL type object for the generator to use
        node = HolderType(kind)

        # Generate declarations
        body.append(helper.generateDecl(node))
        body.append()

        # Generate implementations
        module.append(helper.generateImpl(node))
        module.append()

    header.write(cppcode.SourceFile(open('holders.h', 'w')))
    module.write(cppcode.SourceFile(open('holders.cpp', 'w')))
